
rmdir output\ /s /q

pushd tooling
python3 corpus_creator.py ..\configuration\DSB.yaml
popd
