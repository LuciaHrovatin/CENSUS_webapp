
FROM puckel/docker-airflow:1.10.9
RUN pip install requests
RUN pip install pandas


FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
