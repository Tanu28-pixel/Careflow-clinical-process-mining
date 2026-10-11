
SELECT
  Activity_Name,
  COUNT(*) AS total_events,
  COUNT(DISTINCT Case_ID) AS unique_patients
FROM `careflow-511314.careflow_dataset.raw_event_logs`
GROUP BY Activity_Name
ORDER BY total_events DESC;
