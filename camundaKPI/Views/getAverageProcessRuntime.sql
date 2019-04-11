ALTER VIEW JAR_GET_DATE_DIV_FINISHED_PROCESSESS as
Select 
AP.`PROC_DEF_KEY_` ,
AP.`BUSINESS_KEY_` , 
DATEDIFF(AP.`END_TIME_`, AP.`START_TIME_`) as  ProcessRuntime,
AP.`START_TIME_` as StartTime,
AP.`END_TIME_` as EndTime
from ACT_HI_PROCINST as AP where (AP.`END_TIME_` is not null) and (AP.`SUPER_PROCESS_INSTANCE_ID_` is null) and (AP.`PROC_DEF_KEY_` != 'MassAvailabilityCheck')
 order by AP.`BUSINESS_KEY_`;