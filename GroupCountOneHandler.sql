SELECT MTX_JAM_STAT_DATA."HANDLERNAME", MTX_JAM_STAT_GROUPINGS."GROUPID", COUNT(MTX_JAM_STAT_DATA.ALID) AS COUNT
FROM MTX_JAM_STAT_DATA

LEFT JOIN MTX_JAM_STAT_GROUPINGS ON MTX_JAM_STAT_GROUPINGS."ALID" = MTX_JAM_STAT_DATA."ALID"
WHERE HANDLERNAME = 'MTXA05'
GROUP BY MTX_JAM_STAT_GROUPINGS."GROUPID", MTX_JAM_STAT_DATA."HANDLERNAME"

ORDER BY COUNT DESC