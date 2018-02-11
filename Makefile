root_test: tests/backends/test_ROOT.py

tests/backends/test_ROOT.py: tests/backends/test_numexpr.py
	cat tests/backends/test_numexpr.py | \
		sed 's@LICENSE.@LICENSE.\n# This file is automatically created by "make root_test"@' | \
		sed 's@_numexpr@_root@g' | \
		sed 's@sqrt(@TMath::Sqrt(@g' | \
		sed 's@arctan2(@TMath::ATan2(@g' | \
		sed "s@~@!@g" | \
		sed "s@&@&&@g" | \
		sed "s@|@||@g" \
		> tests/backends/test_ROOT.py
