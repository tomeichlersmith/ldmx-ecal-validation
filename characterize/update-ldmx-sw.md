# Update ldmx-sw
These instructions are for folks who are _not_ developing ldmx-sw but instead simply want
to update to the latest version of ldmx-sw (maybe even the HEAD of trunk). If you are
a developer of ldmx-sw, it will be helpful to learn more about `git` and how to use
it so you know what these steps do and when you need to do them (Spoiler alert:
you don't need to do them everytime you switch branches).

1. Enter the environment
```
source ldmx-sw/scripts/ldmx-env.sh
```
2. Clean the source tree
```
cd ldmx-sw
ldmx clean src
```
3. Download updated commits from GitHub
```
git fetch
```
4. Switch to branch you want to be on
```
git switch trunk
# if git complains about switch not being a valid
# command, use the older name for it `git checkout trunk`
```
5. Update the branch
```
git pull
```
6. Compile and install
```
ldmx cmake -B build -S .
ldmx cmake --build build --target install
```
