# Hawkeye

[![Build Status](https://api.travis-ci.org/Rahul-RB/SE-B2.svg?branch=master)](https://api.travis-ci.org/Rahul-RB/SE-B2)

> Huge thanks to Ganesh for providing expertise in CICD integration (TravisCI).

> Do **NOT** put a Pull Request(PR) from your master branch. <br>
> PR **SHOULD** come from a development branch of yours (i.e. a non-master branch) to my master branch.

### Dependencies
- Check `requirements.txt`

### How to run?
`cd hawkeye/` 
> Add your Database root password into `__init__.py`

`$ export FLASK_APP=run.py`<br>
`$ export FLASK_ENV=development`<br>
`$ flask run`

## Important note to collaborators:
- I've added you as collaborators for ease of pushing in future. 
- Do not `push` directly to `master` branch. I.e., do **NOT** do : `git push upstream master`.
- There's 2 branches including master branch. Lodge Pull Requests to `master` branch.

## What to do when I/someone say "update _your_ master":
- When you `forked` from my repository, you had the version of my repository at that date and time.
- Overtime there's some changes from various members which cause changes into my `master` branch.
- These changes won't be directly reflected into _your_ master branch. To get these changes, here's what you've to do:
    1. `git remote add upstream https://github.com/Rahul-RB/SE-B2.git`
    2. `git fetch upstream`
    3. `git checkout master`
    4. `git rebase upstream/master`
    4.1. IF you see some "Auto-merging, CONFLICT", it means there's been some `merge-conflict`. If this happens, leave it then and there (unless you know to handle merge-conflicts).
	5. `git push -f origin master`
	
- Note how the step `5` pushes into `origin` and **not** `upstream`. This is because, when you `forked` and `cloned` the same into your desktop, the `origin` points to **your** forked repo and by step 1, `upstream` points to the original repository.


## What to do?
* Fork this repository by pressing the fork button on top.

* Then, go to your profile, find the forked repository (it has the same name as the original repository).

* Now, press the `Clone or download` button and copy the URL. Then clone it into a folder by doing:
	
	`git clone <URL>`

* Create a branch, name it as "development" branch.
	
	`git checkout -b development`
	
* Then, do whatever changes you've to do. Check your changes by doing this command, it shows what files you made changes into.

	`git status`
	
* [OPTIONAL] If you do see a file you changed but forgot what exactly you changed, you can refer to that by doing:

	`git diff`
	
* Once you're done with changes and feel good enough to push the code, do these inside the cloned folder:

	`git add .`<br>
	`git commit -m "Put meaningful message here"`<br>
	`git push origin master`

* Then, once the code is reviewed and approved, you can issue a Pull request by doing the following:
	* Go to your forked repository. 
	* Press `Pull Request` button on top.
	* Put a meaningful message, changed done and issue the request.
	* Upon resolving conflicts, the code will be merged.

* An intro to github can be found in this link: 

[![Github Basic](http://img.youtube.com/vi/0fKg7e37bQE/0.jpg)](http://www.youtube.com/watch?v=0fKg7e37bQE)
