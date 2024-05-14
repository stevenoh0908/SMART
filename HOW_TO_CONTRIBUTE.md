# How Can I Download and Contribute this Model?
---

* 우리 조의 SMART Model 작업은 Github를 통해 소스 코드를 관리하고 데이터 역시 관리하게 됩니다.
* 이 저장소를 이용해 작업을 저장하고 변경 사항을 Commit하는 것에 대해서는 아래의 설명을 참조하시기 바랍니다.

## I. 이 Repository Clone하기
* Git은 코드가 어느 정도 완성되기까지 중간 작업물은 로컬에 저장하고, 작업이 완료되었을 때 수정된 코드의 버전을 공용 저장소로 Push, 다른 사람의 버전을 Pull하는 기능 등을 제공합니다.
* 이 Model 코드에 기여하기 위해서는, 이 Repository를 Clone해야 합니다.
* 기본적으로 여러분은 모두 이 Directory의 공동 작업자로 초대된 상태이므로 자유롭게 Clone하고 Push / Pull이 가능하도록 되어 있습니다.
* Github Desktop이나 Git CLI를 사용하여 이 레포지스토리를 원하는 로컬 폴더로 Clone합니다.
```shell
git clone https://github.com/stevenoh0908/SMART.git
```

## II. Git 변경 내역 확인
* Git은 여러 사람의 작업 결과물 버전을 확인할 수 있습니다.
* Git CLI에서는 `git log` 명령을 통하여 현재 변경 이력을 볼 수 있습니다.
```shell
git log
```

## III. 변경 내역 Push해서 공용 저장소에 반영하기
* 변경 내역이 있다면 우선 변경 사항을 Stage하여 '변경됨'을 반영하도록 합니다.
* Github Desktop에서의 Stage는 자동 추적되므로 별도의 작업이 필요치 않습니다.
* Git CLI의 경우 `git add .` 혹은 `git add <filename or directory name>`으로 Stage할 디렉터리나 폴더를 추가해줍니다.
* Git CLI의 경우 '뭐가 변경되었는지, 뭐가 Stage되어 있는지'를 알고 싶으면 `git status`를 치면 됩니다.
* Github Desktop의 경우 변경 사항에 대한 설명을 Commit 메시지로 작성하고 Push 버튼을 누르면 자동으로 반영됩니다. 자세한 사항은 인터넷을 참조하세요.
* Git CLI의 경우 `git commit`으로 Commit 메시지를 입력하고, `git push origin`으로 변경 사항을 Push할 수 있습니다.
	* 짧은 Commit의 경우 `git commit -m "commit message"`로 굳이 별도의 커밋 메시지를 텍스트 편집기로 입력하지 않고 작업을 Commit할 수 있습니다.
* 항상 Push 이전 후술할 Pull을 이용해서 다른 사람의 작업 내역을 내 로컬 저장소에 반영하시기 바랍니다.

## IV. 다른 사람이 변경한 작업 내역 Pull해서 로컬로 가져오기
* 공용 저장소에 다른 사람이 작업을 Commit & Push한 경우 내 로컬 저장소에는 반영되지 않을 수 있습니다.
* 이 경우 '내 로컬 저장소'를 '공용 저장소'와 동기화하는 작업을 해야 하는데, 이를 쉽게 Pull이라고 합니다.
* Github Desktop에는 Pull & Sync 버튼으로 쉽게 해결할 수 있습니다.
* Git CLI의 경우 `git pull origin`으로 공용 저장소의 변경 내역을 로컬 저장소로 가져와 '최신화'할 수 있습니다.
* 항상 내 변경 내역을 커밋하기 이전에 pull하여 작업 내역을 최신화하시기 바랍니다.

## V. Branch 관련
* 필요한 경우 Branch를 나누어 작업하신 뒤 Merge하셔도 됩니다.
* Git Branch와 관련된 내역은 인터넷의 다음 문서: https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-%EB%B8%8C%EB%9E%9C%EC%B9%98%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80 를 참고하시기 바랍니다.

