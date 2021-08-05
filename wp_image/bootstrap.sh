mkdir wordpress
cd wordpress
wp core download
cp ../wp-config.php ./
wp core install --url=${WP_HOME_URL} --title="Live Chat Translation Demo" --admin_user="admin" --admin_password="admin" --admin_email="admin@example.com"
wp theme activate twentynineteen
wp plugin install wordpress-importer --activate
wget https://raw.githubusercontent.com/WPTRT/theme-unit-test/master/themeunittestdata.wordpress.xml
wp import themeunittestdata.wordpress.xml --authors=create
