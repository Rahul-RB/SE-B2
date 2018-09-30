# SE-B2

## Important note to collaborators:
- I've added you as collaborators for ease of pushing in future. 
- Do not `push` directly to `master` branch. I.e., do NOT do : `git push origin master`
- If you do want to directly `push` into this repository, create a branch, push into that branch and then lodge a PR as:

	`git checkout -b <you-branch-name>`

	` Do your changes, add and commit them.`

	`git push origin <your-branch-name>`
- If you get any doubt on what branch you're on, then you can check that by doing `git status`.
- Also, `git status` can be used to check what files you've changed. It'll also show files waiting to be commited and files ready to be pushed.


## What to do?
* Fork this repository by pressing the fork button on top.
* Then, go to your profile, find the forked repository (it has the same name as the original repository). 
* Now, press the `Clone or download` button and copy the URL. Then clone it into a folder by doing:

    `git clone <URL>`

* Then, do whatever changes you've to do. Once you're done with changes and feel good enough to push the code, do these inside the cloned folder:

	`git add .`
	
	`git commit -m "Put meaningful message here"`
	
	`git push origin master`

* Then, once the code is reviewed and approved, you can issue a Pull request by doing the following:
	* Go to your forked repository. 
	* Press `Pull Request` button on top.
	* Put a meaningful message, changed done and issue the request.
	* Upon resolving conflicts, the code will be merged.

* An intro to github can be found in this link: 

[![Github Basic](http://img.youtube.com/vi/0fKg7e37bQE/0.jpg)](http://www.youtube.com/watch?v=0fKg7e37bQE)
