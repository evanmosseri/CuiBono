download_files:
	mkdir -p data/texas_ethics_commission
	curl -o data/TEC_CF_CSV.zip "https://www.ethics.state.tx.us/tedd/TEC_CF_CSV.zip" --insecure
	unzip data/TEC_CF_CSV.zip -d data/texas_ethics_commisions
	rm -rf data/TEC_CF_CSV.zip
	git log > IDB1.log

Models.html: CuiBono/models/models.py 
	pydoc3 -w CuiBono/models/models.py

clean:
	rm -rf data/texas_ethics_commission
