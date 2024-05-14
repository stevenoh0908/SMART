# SMART
2024-1 SNU Atmospheric Physics I Term Project - Single-column Multi-layered Atmospheric Radiative Transfer (SMART) Model
---

## List of Contributers
- Yooshin Oh
- Yoonsung Lee
- Hyeongjoon Byeon
- Dongwon Kang

## TODO
1. Construct the code of SMART Model
	- Construct FDM Module: Yooshin Oh
	- Construct J-Calculation Module: Dongwon Kang
2. Finding Initial Conditions: Hyeongjoon Byeon, Yoonsung Lee
	- Find Initial Temperature Profile ($T(0, z)$)
	- Calculate $c_p(z)$, $R(z)$
		- This should be followed by $\bar{M}(z)$ and $\omega_{material}(z)$, $\rho_{air}(z)$, $k_{a, material}$.
		- If needed, add some appropriate assumption to make a initial profile of above quantities.
		- Also Total Number of the vertical Cell and the Maximum Heights should be determined from the available references of the above quantities.
	- If needed, contact to the professor to find out the references.
3. Integrating Initial Condition Arrays and Modules & Debugging: Yooshin Oh
4. Plotting Result, Making Slides & Preparing the Presentation: All Contributors (?)

## Direction of the project
1. 산불이 났을 때 Black Carbon이 방출될 경우 Multi-layered RT Model에서 온도와 지표온 Profile
2. 화산 폭발의 에어로졸이 성층권 등에 유입될 경우 SW 반사 효과를 무시할 때 Multi-layered RT Model의 계산된 대기 온도 Profile, 지표온의 알려진 연구와의 비교를 통해 SW의 중요성 평가하기

## Major Assumptions of this Model
1. No Reflection or Scattering are considered except for SW Reflection on the Surface due to the Planetory Albedo.
2. Neglect the Vertical Motion of the Atmosphere ($w \approx 0$) -> Therefore no Mixing is Occured
3. The $c_p(z)$, $R(z)$ profile is a function only depends on the vertical cooridnate
4. Single-column Model, therefore assuming all quantities are constant among the same height.
5. Assuming there's no latent process.

## NOTE
- For the equations of the SMART model, please refer to the model derivation sheet that we've shared already.
- Please follow the pre-determined interface to make the whole work a lot easier.
- This Module will be developed and tested in the following environment.
	- Python 3.10.12
	- Numpy 1.26.3
	- Matplotlib 3.8.2
	- PyYAML 5.4.1
- 모든 코드에 Commenting을 잘 달아주시기 바랍니다. Code Integration과 Debugging의 시간을 단축하고자 합니다.
