ALTER VIEW JAR_GET_IIDS_BY_FINISHED_PROCESSES AS
Select AHP.`PROC_INST_ID_` as InstanceID,
AHP.`BUSINESS_KEY_` as BusinessKey ,
AHP.`PROC_DEF_KEY_` as ProcessName,
AHP.`START_TIME_` as StartTime,
AHP.`END_TIME_` as EndTime
from ACT_HI_PROCINST as AHP where 
AHP.`BUSINESS_KEY_` in (Select AP.`BUSINESS_KEY_` from ACT_HI_PROCINST as AP where (AP.`END_TIME_` is not null) and (AP.`SUPER_PROCESS_INSTANCE_ID_` is null) and (AP.`PROC_DEF_KEY_` != 'MassAvailabilityCheck'))
 order by AHP.`BUSINESS_KEY_` 