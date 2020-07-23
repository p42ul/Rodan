# rodan website
New project site for Rodan. 

For local development, install [Jekyll](http://jekyllrb.com/), and in the root directory of this branch run
```
jekyll serve -w --baseurl /
```

Using [uncss](https://github.com/giakki/uncss) to remove unused Bootstrap rules using the following command:

```
uncss -s css/bootstrap.css http://ddmal.github.io/rodan/ http://ddmal.github.io/rodan/download http://ddmal.github.io/rodan/doc http://ddmal.github.io/rodan/about > minified.css
```
