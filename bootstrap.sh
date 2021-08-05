cd wp_image
wget http://wordpress.org/latest.tar.gz
tar xzf latest.tar.gz
mv wordpress/wp-content/themes/twentynineteen ./
rm -r wordpress latest.tar.gz

cd ../lhc_image
git clone https://github.com/LiveHelperChat/livehelperchat.git
mv livehelperchat/lhc_web ./
rm -rf livehelperchat
