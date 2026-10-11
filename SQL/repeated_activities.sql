SELECT
  Case_ID,
  Activity_Name,
  COUNT(*) AS activity_count
FROM `careflow-511314.careflow_dataset.raw_event_logs`
GROUP BY Case_ID, Activity_Name
HAVING COUNT(*) > 1
ORDER BY activity_count DESC, Case_ID;