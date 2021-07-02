from saver import MySQLManager

saver = MYSQL

"SELECT CONCAT(
 '*10\r\n',
   '$', LENGTH(redis_cmd), '\r\n', redis_cmd, '\r\n',
   '$', LENGTH(redis_key), '\r\n', redis_key, '\r\n',
   '$', LENGTH(hkey1),'\r\n',hkey1,'\r\n','$',LENGTH(hval1),'\r\n',hval1,'\r\n',
   '$', LENGTH(hkey2),'\r\n',hkey2,'\r\n','$',LENGTH(hval2),'\r\n',hval2,'\r\n',
   '$', LENGTH(hkey3),'\r\n',hkey3,'\r\n','$',LENGTH(hval3),'\r\n',hval3,'\r\n',
   '$', LENGTH(hkey4),'\r\n',hkey4,'\r\n','$',LENGTH(hval4),'\r\n',hval4,'\r\n',
    '$', LENGTH(hkey5),'\r\n',hkey5,'\r\n','$',LENGTH(hval5),'\r\n',hval5,'\r\n',
    '$', LENGTH(hkey6),'\r\n',hkey6,'\r\n','$',LENGTH(hval6),'\r\n',hval6,'\r\n',
    '$', LENGTH(hkey7),'\r\n',hkey7,'\r\n','$',LENGTH(hval7),'\r\n',hval7,'\r\n',
    '$', LENGTH(hkey8),'\r\n',hkey8,'\r\n','$',LENGTH(hval8),'\r\n',hval8,'\r\n',
    '$', LENGTH(hkey9),'\r\n',hkey9,'\r\n','$',LENGTH(hval9),'\r\n',hval9,'\r\n',
    '$', LENGTH(hkey10),'\r\n',hkey10,'\r\n','$',LENGTH(hval10),'\r\n',hval10,'\r'
)
FROM (
 SELECT
 'HSET' AS redis_cmd,
 CONCAT('{}:info:',id) AS redis_key,
 'nquest' AS hkey1, nquest AS hval1,
 'ncomp' AS hkey2, ncomp AS hval2,
 'nord' AS hkey3, nord AS hval3,
 'sex' AS hkey4, sex AS hval4,
 'anasc' AS hkey5, anasc AS hval5,
 'staciv' AS hkey6, staciv AS hval6,
 'ireg' AS hkey7, ireg AS hval7,
 'perc' AS hkey8, staciv AS hval8,
 'area5' AS hkey9, area5 AS hval9,
 'Y' AS hkey10, Y AS hval10
 FROM `{}`
) AS t".format(table_name, table_name)