PATH=$(npm bin):$PATH

npm install
gulp
(cd design/defaulttheme/widget/wrapper && npm install && npm run build)
(cd design/defaulttheme/widget/react-app && npm install && npm run build)
php cron.php -s site_admin -c cron/util/generate_css -p 1
gulp js-static

