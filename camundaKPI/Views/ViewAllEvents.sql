CREATE VIEW JAR_SHOW_ALL_EVENTS_BY_ID AS
 Select Z.`ACT_ID_`,Z.`ACT_NAME_` From ACT_HI_ACTINST as Z where Z.`ACT_TYPE_` in ('intermediateNoneThrowEvent','startEvent','noneEndEvent') and Z.ACT_NAME_ is not null
 group by Z.ACT_ID_

CREATE VIEW JAR_BK_WITH_INSTANCEIDS AS
select JFP.`BusinessKey`,JFP.`InstanceID` from `JAR_GET_IIDS_BY_FINISHED_PROCESSES` as JFP
	
	
CREATE VIEW JAR_EVENT_SELECTION_ACTIVITY_HISTORY AS
select Z.`ACT_ID_`,Z.`PROC_INST_ID_`,Z.`ACT_NAME_`,Z.`START_TIME_`,Z.`END_TIME_` From ACT_HI_ACTINST as Z where Z.`ACT_TYPE_` in ('intermediateNoneThrowEvent','startEvent','noneEndEvent') and Z.ACT_NAME_ is not null

CREATE VIEW JAR_EVENTS_BY_BUSINESSKEY AS
Select * 
from 
	JAR_BK_WITH_INSTANCEIDS as I
	inner join 
	JAR_EVENT_SELECTION_ACTIVITY_HISTORY as E
	on E.`PROC_INST_ID_`=I.`InstanceID` 


CREATE TABLE IF NOT EXISTS KPI (
    KPI_id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    START_ACT_ID_ VARCHAR(225) NOT NULL,
    END_ACT_ID_ VARCHAR(225) NOT NULL,
    KPI_VALUE INT NOT NULL,
    PRIMARY KEY (KPI_id)
)  ENGINE=INNODB;



(Select * from 
`JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as A
inner join 
`KPI` as K ON K.`START_ACT_ID_` = A.`ACT_ID_`)
Union 
(Select * from 
`JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as B
 inner join 
`KPI` as K2 ON K2.`END_ACT_ID_` = B.`ACT_ID_`)

--KPI-Select Statement
Select 
X.BusinessKey as BusinessKey,
X.`ACT_ID_` as StartactivityID,
Y.`ACT_ID_` as EndactivityID,
X.`ACT_NAME_`as StartName,
Y.`ACT_NAME_` as EndName,
X.`START_TIME_` as StartTime,
Y.`END_TIME_` as EndTime,
X.`KPI_id` as KpiID,
hour(TIMEDIFF(Y.`END_TIME_`,X.`START_TIME_`)) as DifferenzInStunden,
DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) as DifferenzInTagen,
CASE WHEN (DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) <= X.`KPI_VALUE`) THEN 'false'
ELSE 'true' END as KpiBroken,
'' as updateRun
from 
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as A
				inner join JAR_BK_WITH_INSTANCEIDS as O
							ON A.`PROC_INST_ID_` = O.`InstanceID`
				inner join `KPI` as K 
							ON K.`START_ACT_ID_` = A.`ACT_ID_`) AS X
	inner join  
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as B
				inner join JAR_BK_WITH_INSTANCEIDS as I
							ON B.`PROC_INST_ID_` = I.`InstanceID`
				inner join `KPI` as K2 
 							ON K2.`END_ACT_ID_` = B.`ACT_ID_`) AS Y
on Y.`BusinessKey`= X.`BusinessKey` and Y.`KPI_id` = X.`KPI_id`

CREATE TABLE IF NOT EXISTS JAR_KPI_REPORT (
    KPI_REPORT_ID bigint AUTO_INCREMENT, 
    BusinessKey varchar(255) ,
    StartactivityID VARCHAR(225) NOT NULL,
    EndactivityID VARCHAR(225) NOT NULL,
    StartName VARCHAR(225) NOT NULL,
    EndName VARCHAR(225) NOT NULL,
    StartTime date NOT NULL,
    EndTime date NOT NULL,
    KpiID int not null,
    DifferenzInStunden int not null,
    DifferenzInTagen int not null,
    KpiBroken boolean not null,
    updateRun date not null,
    PRIMARY KEY (KPI_REPORT_ID)
)  ENGINE=INNODB;



INSERT INTO `JAR_KPI_REPORT` (`BusinessKey`,`StartactivityID`,`EndactivityID`,`StartName`,`EndName`,`StartTime`,`EndTime`,`KpiID`,`DifferenzInStunden`,`DifferenzInTagen`,`KpiBroken`,`updateRun`) 
Select 
X.BusinessKey as BusinessKey,
X.`ACT_ID_` as StartactivityID,
Y.`ACT_ID_` as EndactivityID,
X.`ACT_NAME_`as StartName,
Y.`ACT_NAME_` as EndName,
X.`START_TIME_` as StartTime,
Y.`END_TIME_` as EndTime,
X.`KPI_id` as KpiID,
hour(TIMEDIFF(Y.`END_TIME_`,X.`START_TIME_`)) as DifferenzInStunden,
DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) as DifferenzInTagen,
CASE WHEN (DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) <= X.`KPI_VALUE`) THEN '0'
ELSE '1' END as KpiBroken,
'asdasdasd' as updateRun
from 
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as A
				inner join JAR_BK_WITH_INSTANCEIDS as O
							ON A.`PROC_INST_ID_` = O.`InstanceID`
				inner join `KPI` as K 
							ON K.`START_ACT_ID_` = A.`ACT_ID_`) AS X
	inner join  
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as B
				inner join JAR_BK_WITH_INSTANCEIDS as I
							ON B.`PROC_INST_ID_` = I.`InstanceID`
				inner join `KPI` as K2 
 							ON K2.`END_ACT_ID_` = B.`ACT_ID_`) AS Y
on Y.`BusinessKey`= X.`BusinessKey` and Y.`KPI_id` = X.`KPI_id`