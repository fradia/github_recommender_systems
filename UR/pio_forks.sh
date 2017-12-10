echo "Checking for needed files"
if [ ! -f examples/forks-engine-simple.json ]; then
    echo "File not found: engines/forks-engine-simple.json"
    exit 1
fi

if [ ! -f data/forks_sample.csv ]; then
    echo "File not found: data/forks_sample_prepared_train.csv"
    exit 1
fi

if [ -f user-engine.json ]; then
    echo "File user-engine.json found, this may be an error so we cannot replace engine.json"
    exit 1
fi

echo ""
echo "Checking status, should exit if pio is not running."
pio status
pio app new forks || true

echo ""
echo "Checking to see if forks app exists, should exit if not."
pio app show forks

echo ""
echo "Moving engine.json to user-engine.json if it exists"
cp -n engine.json user-engine.json || true

echo ""
echo "Moving engines/forks-engine-simple.json to engine.json for integration test."
cp examples/forks-engine-simple.json engine.json

echo ""
echo "Deleting handmade app data since the test is date dependent"
pio app data-delete forks -f

echo ""
echo "Importing data for integration test"
# get the access_key from pio app list
ACCESS_KEY=`pio app show forks | grep Key | cut -f 7 -d ' '`
echo -n "Access key: "
echo $ACCESS_KEY
python import_data.py --access_key $ACCESS_KEY --file data/forks_sample.csv

echo ""
echo "Building and delpoying model"
pio build
pio train  -- --driver-memory 4g --executor-memory 4g
echo "Model will remain deployed after this test"
nohup pio deploy > deploy.out &
echo "Waiting 50 seconds for the server to start"
sleep 50
echo "Ready to export recommendations..."


