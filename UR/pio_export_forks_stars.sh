echo "Export recommendations"
python export_predictions.py --file_i data/forks_stars_sample.csv --file_o data/ur_forks_stars_rec.json

echo ""
echo "Restoring engine.json if is was saved"
mv user-engine.json engine.json || true 
