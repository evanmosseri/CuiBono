ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif

download_files:
	mkdir -p data/texas_ethics_commission
	curl -o data/TEC_CF_CSV.zip "https://www.ethics.state.tx.us/tedd/TEC_CF_CSV.zip" --insecure
	unzip data/TEC_CF_CSV.zip -d data/texas_ethics_commisions
	rm -rf data/TEC_CF_CSV.zip
	git log > IDB1.log

.pylintrc:
	$(PYLINT) --disable=no-name-in-module,global-statement,mixed-indentation,redefined-outer-name,bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

tests.tmp: .pylintrc tests.py
	-$(PYLINT) tests.py
	$(COVERAGE) run  --omit='*numpy*' --branch tests.py > TestResult.out 2>&1
	$(COVERAGE) report -m                      >> TestResult.out
	cat TestResult.out


Models.html: CuiBono/models/models.py 
	pydoc3 -w CuiBono/models/models.py


clean:
	rm -rf data/texas_ethics_commission
