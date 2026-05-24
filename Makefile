# .envファイルがあれば読み込む
ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: build publish-test publish clean

build:
	uv build

# TestPyPIへのアップロード
# 環境変数 TEST_PYPI_TOKEN を使用
publish-test: build
	uv publish --publish-url https://test.pypi.org/legacy/ --token $(TEST_PYPI_TOKEN) dist/*

# 本番PyPIへのアップロード
# 環境変数 PYPI_TOKEN を使用
publish: build
	uv publish --token $(PYPI_TOKEN) dist/*

clean:
	rm -rf dist/ build/ ./*.egg-info
