FROM node:10 as builder
WORKDIR /app

ADD lhc_web /app
COPY lh.js /app/design/defaulttheme/js/lh.js
COPY chatWidgetReducer.js /app/design/defaulttheme/widget/react-app/src/reducers/chatWidgetReducer.js
COPY build.sh /app/build.sh

ARG TRANSLATE_SERVICE_URL
RUN echo $TRANSLATE_SERVICE_URL
RUN sed -e "s|\${process.env.TRANSLATE_SERVICE_URL}|$TRANSLATE_SERVICE_URL|" -i /app/design/defaulttheme/widget/react-app/src/reducers/chatWidgetReducer.js
RUN sed -e "s|\${process.env.TRANSLATE_SERVICE_URL}|$TRANSLATE_SERVICE_URL|" -i /app/design/defaulttheme/js/lh.js

RUN apt update -y && apt install php -y
RUN ./build.sh
RUN find . -name "node_modules" -type d -prune -exec rm -rf '{}' +

FROM webdevops/php-apache
COPY --chown=application:application --from=builder /app /app
# Uncomment below line for second build, after installation is complete
# COPY settings.ini.php /app/settings/settings.ini.php
COPY htaccess /app/.htaccess
