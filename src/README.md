# src Structure
```
src ... where the whole source of the model is located at.
|_ common ... common constants and methods
|_ fdm ... finite difference method model, All fdm-calculation methods and classes are located in here.
|_ rt ... radiative transfer calculation model, All rt-related method (including J-calculation method) and classes are located in here.
|_ load ... initial condition loading model. The initial profiles of the quantities are loaded from the module included in this directory.
|_ config.yml ... configuration file of the model (yml file)
|_ main.py ... main driver of the SMART model
```

# Interfaces
- 초기 조건의 로드
	- 모든 초기 조건은 Initial Timestep ($t = 0$) 에서 \n (개행문자)로 분리된 txt 파일로 값을 작성합니다.
		- 모든 초기 조건 파일은 표준 SI 단위로 작성합니다.
	- 이를테면, 초기 온도 profile의 경우 13개 층을 가정한 경우, 지표 포함 총 14개의 층이 있으므로 지표 온도부터 차례대로 층을 올려가며 K 단위로
		```
		300.15
		297.5
		298.1
		...
		```
		위와 같이 작성하여 특정 파일 이름으로 저장합니다.
		각 초기 조건은 src 디렉터리 위에 있는 data directory에 넣은 txt 파일을 config.yml로 지정한 파일 이름으로 읽어서 로드하게 됩니다.
- J-calculation Model (Updated on 16 May 2024)
	- J-calculation Model은 다음의 입력을 받습니다.
		1. Timestep Index (Not a timestep)
		2. Height Index (Not a height)
		3. Timestep Interval ($\Delta t$)
		4. Height Interval ($\Delta z$)
		5. $c_p(z)$ Array
		6. $R(z)$ Array
		7. $a_{sw}(z)$ Array
		8. $a_{lw}(z)$ Array
		9. $T(t, z)$ Array
		10. $\Delta x$, $\Delta y$ (or, the cross-section of the layer)
	- J-calculation에서 16일 교수님의 조언에 따라 $\beta_{a}$ Profile을 찾기 보다는 상황에 따라 SW / LW에서 Absorptivity Profile을 적절히 가정하여 계산하는 것으로 변경하였습니다.
	- J-calculation Model은 주어진 Timestep Index와 Height Index에서의 '그 Layer의 Net Flux'를 표준 SI 단위인 J/s로 계산해야 합니다.
- Driver 모듈과 Loader, FDM 모듈은 상기 Interface 규약에 따라 설계될 예정이니 참고 바랍니다.
