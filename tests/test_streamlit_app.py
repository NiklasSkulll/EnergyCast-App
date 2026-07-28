import unittest

from streamlit.testing.v1 import AppTest


class EnergyCastStreamlitAppTests(unittest.TestCase):
    def test_app_renders_main_page_without_exceptions(self):
        # Break caught: top-level Streamlit import/runtime errors in the dashboard entry point.
        app = AppTest.from_file("app/streamlit_app.py")
        app.run(timeout=90)

        titles = [title.value for title in app.title]
        self.assertEqual(len(app.exception), 0)
        self.assertIn("EnergyCast Scenario Forecast", titles)

    def test_app_is_scenario_forecast_tool_not_model_performance_report(self):
        # Break caught: turning the app into a modeling-statistics dashboard or 2019 replay tool.
        app = AppTest.from_file("app/streamlit_app.py")
        app.run(timeout=90)

        titles = [title.value for title in app.title]
        tab_labels = [tab.label for tab in app.tabs]
        metric_labels = [metric.label for metric in app.metric]
        widget_labels = (
            [widget.label for widget in app.date_input]
            + [widget.label for widget in app.slider]
            + [widget.label for widget in app.radio]
        )

        self.assertEqual(len(app.exception), 0)
        self.assertIn("EnergyCast Scenario Forecast", titles)
        self.assertIn("Scenario Forecast", tab_labels)
        self.assertIn("Generated Inputs", tab_labels)
        self.assertIn("Forecast start date", widget_labels)
        self.assertIn("Demand growth per year (%)", widget_labels)
        self.assertIn("Temperature shift (C)", widget_labels)
        self.assertIn("Renewable generation scale (%)", widget_labels)
        self.assertIn("Peak forecast", metric_labels)
        self.assertIn("Forecasted energy", metric_labels)
        self.assertNotIn("Executive Summary", tab_labels)
        self.assertNotIn("Error Diagnostics", tab_labels)
        self.assertNotIn("Model Evidence", tab_labels)
        self.assertNotIn("Input Context", tab_labels)
        self.assertNotIn("Current sMAPE", metric_labels)
        self.assertNotIn("Current MAE", metric_labels)
        self.assertNotIn("2019 sMAPE", metric_labels)


if __name__ == "__main__":
    unittest.main()
