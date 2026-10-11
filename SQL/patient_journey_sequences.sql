SELECT
  Case_ID,
  STRING_AGG(Activity_Name, ' → ' ORDER BY Timestamp) AS patient_journey,
  COUNT(*) AS total_steps
FROM `careflow-511314.careflow_dataset.raw_event_logs`
GROUP BY Case_ID
ORDER BY total_steps DESC, Case_ID
LIMIT 20;