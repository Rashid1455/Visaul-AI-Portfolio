import json
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from orders import save_order
from service_catalog import load_catalog, validate_selection
from streamlit.testing.v1 import AppTest

def payload():
    return dict(service_id="ai-videos", selection=dict(option="Social video", dimensions="1080x1920", quantity=1, duration_seconds=30, requirements="A short product video", custom_requirements=False), customer=dict(name="Client",email="client@example.com",phone="+92 123456789"),consent=True)

class OrderTests(unittest.TestCase):
    def test_all_service_pages_and_sample_files(self):
        project = Path(__file__).resolve().parents[1]
        for slug, service in load_catalog()['services'].items():
            with self.subTest(service=slug):
                for sample in service['samples']:
                    self.assertTrue((project/'portfolio_uploads'/sample).is_file(), sample)
                app = AppTest.from_file(str(project/'app.py'), default_timeout=20)
                app.query_params['service'] = slug
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(app.title[0].value, service['title'])
                app.button[0].click().run()
                self.assertTrue(app.warning)
                self.assertFalse(app.exception)

    def test_unknown_url_and_navigation(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'), default_timeout=20)
        app.query_params['service'] = 'unknown-service'
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(app.info)
        app.sidebar.radio[0].set_value('Home').run()
        self.assertFalse(app.exception)
        self.assertNotIn('service', app.query_params)

    def test_edit_preserves_options_and_custom_quote(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'), default_timeout=20)
        app.query_params['service'] = 'ai-videos'
        app.run()
        app.slider[0].set_value(120)
        app.number_input[0].set_value(3)
        app.text_area[0].set_value('Custom launch campaign')
        app.checkbox[0].check().run()
        self.assertEqual(app.metric[0].value, 'Request a quote')
        app.button[0].click().run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.slider[0].value, 120)
        self.assertEqual(app.number_input[0].value, 3)
        self.assertEqual(app.text_area[0].value, 'Custom launch campaign')
        self.assertTrue(app.checkbox[0].value)

    def test_invalid_selection_boundaries(self):
        for changes in ({'quantity':0}, {'quantity':101}, {'quantity':True}, {'quantity':1.5},
                        {'option':'unknown'}, {'dimensions':'unknown'}, {'requirements':'   '},
                        {'requirements':'x'*10001}, {'custom_requirements':'yes'}):
            with self.subTest(changes=str(changes)[:100]), self.assertRaises(ValueError):
                validate_selection('ai-videos', dict(payload()['selection'], **changes))

    def test_backup_failure_retry_preserves_original(self):
        import orders
        real_publish = orders.publish_json
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'PORTFOLIO_ORDER_BACKEND':'json', 'PORTFOLIO_BACKUP_DIR':str(Path(folder)/'backups')}):
            root = Path(folder)
            reference = str(uuid4())
            def fail_backup(path, record):
                if path.parent.name == 'backups':
                    raise OSError('Simulated unavailable backup storage')
                return real_publish(path, record)
            with patch('orders.publish_json', side_effect=fail_backup), self.assertRaises(OSError):
                save_order(root, reference, payload())
            original = json.loads(next(root.glob('*.json')).read_text())
            saved = save_order(root, reference, payload())
            self.assertEqual(saved, original)
            self.assertEqual(json.loads(next((root/'backups').glob('*.json')).read_text()), original)
            self.assertFalse(list(root.rglob('*.tmp')))

    def test_private_storage_and_consent(self):
        project = Path(__file__).resolve().parents[1]
        for name in ('static','public','portfolio_uploads','.git'):
            with self.subTest(directory=name), self.assertRaises(ValueError):
                save_order(project/name/'test-orders', str(uuid4()), payload())
        with tempfile.TemporaryDirectory() as folder:
            data = payload()
            data['consent'] = False
            with self.assertRaises(ValueError):
                save_order(Path(folder), str(uuid4()), data)
            self.assertFalse(list(Path(folder).iterdir()))

    def test_price_bounds_and_quote(self):
        selection = payload()["selection"]
        for duration in (2,30,300):
            _, price = validate_selection("ai-videos",dict(selection,duration_seconds=duration))
            self.assertEqual(price["estimated_total"],duration*500)
        for duration in (1,301,True):
            with self.assertRaises(ValueError):
                validate_selection("ai-videos",dict(selection,duration_seconds=duration))
        self.assertTrue(validate_selection("ai-videos",dict(selection,dimensions="Custom"))[1]["quote_required"])

    def test_concurrent_retries_and_backup(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"PORTFOLIO_ORDER_BACKEND":"json"}):
            root=Path(folder)
            reference=str(uuid4())
            with ThreadPoolExecutor(max_workers=4) as workers:
                records=list(workers.map(lambda _:save_order(root,reference,payload()),range(8)))
            self.assertTrue(all(r==records[0] for r in records))
            self.assertEqual(len(list(root.glob('*.json'))),1)
            self.assertEqual(json.loads(next((root/'backups').glob('*.json')).read_text()),records[0])
            self.assertEqual(records[0]['payment_status'],'unpaid')

    def test_sqlite_and_untrusted_status(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"PORTFOLIO_ORDER_BACKEND":"sqlite"}):
            data=payload()
            data.update(payment_status='paid',pricing={'estimated_total':0})
            record=save_order(Path(folder),str(uuid4()),data)
            self.assertEqual(record['payment_status'],'unpaid')
            self.assertEqual(record['pricing']['estimated_total'],15000)
            self.assertTrue((Path(folder)/'orders.sqlite3').exists())

    def test_invalid_customer(self):
        with tempfile.TemporaryDirectory() as folder:
            data=payload(); data['customer']['email']='invalid'
            with self.assertRaises(ValueError):
                save_order(Path(folder),str(uuid4()),data)
            self.assertFalse(list(Path(folder).iterdir()))

    def test_service_url_and_order_journey(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'PORTFOLIO_ORDER_DIR':folder,'PORTFOLIO_ORDER_BACKEND':'json'}):
            app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=20)
            app.query_params['service']='ai-videos'
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.sidebar.radio[0].value,'Service details')
            app.slider[0].set_value(60).run()
            self.assertEqual(app.metric[0].value,'PKR 30,000')
            app.text_area[0].set_value('A product launch film')
            app.button[0].click().run()
            app.text_input[0].set_value('Client')
            app.text_input[1].set_value('client@example.com')
            app.checkbox[0].check()
            app.button[-1].click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.success)
            record=json.loads(next(Path(folder).glob('*.json')).read_text())
            self.assertEqual(record['selection']['duration_seconds'],60)
            app.run()
            self.assertEqual(len(list(Path(folder).glob('*.json'))),1)
