demo3:
	@echo "Running Demo with 3 sensors"
	python3 mainCli.py --drive savedNet/3-100-50-10-1-0_001-trackMaster/440.txt -n np

demo21:
	@echo "Running Demo with 3 sensors"
	python3 mainCli.py --drive saveNetTFII/21-100-50-20-1-0_001-21SensorsAngle636844638113218400/model-999

demoTrain:
	@echo 'Train network with graphics'
	python3 mainCli.py --train datasets/sensors03/trackMaster1k.txt --learningrate 0.001 --epochs 20 --shape 3 20 10 1 --network tf --graphic

git-clean:
	@echo "Removing merged branches ..."
	git branch --merged master | grep -v 'master$$' | xargs git branch -d
	git fetch --prune --quiet

