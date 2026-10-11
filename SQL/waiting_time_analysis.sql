SELECT
  Case_ID,
  Activity_Name,
  Timestamp,
  LEAD(Activity_Name) OVER (
    PARTITION BY Case_ID ORDER BY Timestamp
  ) AS next_activity,
  LEAD(Timestamp) OVER (
    PARTITION BY Case_ID ORDER BY Timestamp
  ) AS next_timestamp,
  TIMESTAMP_DIFF(
    LEAD(Timestamp) OVER (
      PARTITION BY Case_ID ORDER BY Timestamp
    ),
    Timestamp,
    MINUTE
  ) AS minutes_to_next_activity
FROM `careflow-511314.careflow_dataset.raw_event_logs`
ORDER BY Case_ID, Timestamp;