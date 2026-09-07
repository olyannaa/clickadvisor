---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-a-chatbot-for-hacker-news-and-stack-overflow-with-llamaindex-and-clickhouse-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 7
total_chunks_in_doc: 18
---

questions such as “What were people in 2022 saying about the most popular web technology?” We leave this an exercise for the enthusiastic reader. This data contains a significant number of columns as shown in the schema below:

```
1CREATE TABLE surveys
2(
3   `response_id` Int64,
4   `development_activity` Enum8('I am a developer by profession' = 1, 'I am a student who is learning to code' = 2, 'I am not primarily a developer, but I write code sometimes as part of my work' = 3, 'I code primarily as a hobby' = 4, 'I used to be a developer by profession, but no longer am' = 5, 'None of these' = 6, 'NA' = 7),
5   `employment` Enum8('Independent contractor, freelancer, or self-employed' = 1, 'Student, full-time' = 2, 'Employed full-time' = 3, 'Student, part-time' = 4, 'I prefer not to say' = 5, 'Employed part-time' = 6, 'Not employed, but looking for work' = 7, 'Retired' = 8, 'Not employed, and not looking for work' = 9, 'NA' = 10),
6   `country` LowCardinality(String),
7   `us_state` LowCardinality(String),
8   `uk_county` LowCardinality(String),
9   `education_level` Enum8('Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)' = 1, 'Bachelor's degree (B.A., B.S., B.Eng., etc.)' = 2, 'Master's degree (M.A., M.S., M.Eng., MBA, etc.)' = 3, 'Other doctoral degree (Ph.D., Ed.D., etc.)' = 4, 'Some college/university study without earning a degree' = 5, 'Something else' = 6, 'Professional degree (JD, MD, etc.)' = 7, 'Primary/elementary school' = 8, 'Associate degree (A.A., A.S., etc.)' = 9, 'NA' = 10),
10   `age_started_to_code` Enum8('Younger than 5 years' = 1, '5 - 10 years' = 2, '11 - 17 years' = 3, '18 - 24 years' = 4, '25 - 34 years' = 5, '35 - 44 years' = 6, '45 - 54 years' = 7, '55 - 64 years' = 8, 'Older than 64 years' = 9, 'NA' = 10),
11   `how_learned_to_code` Array(String),
12   `years_coding` Nullable(UInt8),
13   `years_as_a_professional_developer` Nullable(UInt8),
14   `developer_type` Array(String),
15   `organization_size` Enum8('Just me - I am a freelancer, sole proprietor, etc.' = 1, '2 to 9 employees' = 2, '10 to 19 employees' = 3, '20 to 99 employees' = 4, '100 to 499 employees' = 5, '500 to 999 employees' = 6, '1,000 to 4,999 employees' = 7, '5,000 to 9,999 employees' = 8, '10,000 or more employees' = 9, 'I don't know' = 10, 'NA' = 11),
16   `compensation_total` Nullable(UInt64),
17   `compensation_frequency` Enum8('Weekly' = 1, 'Monthly' = 2, 'Yearly' = 3, 'NA' = 4),
18   `language_have_worked_with` Array(String),
19   `language_want_to_work_with` Array(String),
20   `database_have_worked_with` Array(String),
21   `database_want_to_work_with` Array(String),
22   `platform_have_worked_with` Array(String),
23   `platform_want_to_work_with` Array(String),
24   `web_framework_have_worked_with` Array(String),
25   `web_framework_want_to_work` Array(String),
26   `other_tech_have_worked_with` Array(String),
27   `other_tech_want_to_work` Array(String),
28   `infrastructure_tools_have_worked_with` Array(String),
29   `infrastructure_tools_want_to_work_with` Array(String),
30   `developer_tools_have_worked_with` Array(String),
31   `developer_tools_want_to_work_with` Array(String),
32   `operating_system` Enum8('MacOS' = 1, 'Windows' = 2, 'Linux-based' = 3, 'BSD' = 4, 'Other (please specify):' = 5, 'Windows Subsystem for Linux (WSL)' = 6, 'NA' = 7),
33   `frequency_visit_stackoverflow` Enum8('Multiple times per day' = 1, 'Daily or almost daily' = 2, 'A few times per week' = 3, 'A few times per month or weekly' = 4, 'Less than once per month or monthly' = 5, 'NA' = 6),
34   `has_stackoverflow_account` Enum8('Yes' = 1, 'No' = 2, 'Not sure/can\'t remember' = 3, 'NA' = 4),
35   `frequency_use_in_stackoverflow` Enum8('Multiple times per day' = 1, 'Daily or almost daily' = 2, 'A few times per week' = 3, 'A few times per month or weekly' = 4, 'Less than once per month or monthly' = 5, 'I have never participated in Q&A on Stack Overflow' = 6, 'NA' = 7),
36   `consider_self_active_community_member` Enum8('Yes, definitely' = 1, 'Neutral' = 2, 'Yes, somewhat' = 3, 'No, not at all' = 4, 'No, not really' = 5, 'NA' = 6, 'Not sure' = 7),
37   `member_other_communities` Enum8('Yes' = 1, 'No' = 2, 'NA' = 4),
38   `age` Enum8('Under 18 years old' = 1, '18-24 years old' = 2, '25-34 years old' = 3, '35-44 years old' = 4, '45-54 years old' = 5, '55-64 years old' = 6, '65 years or older' = 7, 'NA' = 8, 'Prefer not to say' = 9),
39   `annual_salary` Nullable(UInt64)
40)
41ENGINE = MergeTree
42ORDER BY tuple()
```
Copy command
