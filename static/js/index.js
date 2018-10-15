window.onload=function () {
    //水果轮播图
    let fruit=document.querySelector(".fruit");
    let img=document.querySelectorAll(".fruit img");
    let bg=document.querySelectorAll(".bg");
    let first=document.querySelectorAll(".first");
    console.log(fruit, img, bg);
    let next=now=0;

    fruit.onclick=function () {
        next++;
        if(next==img.length){
            next=0;
        }
        bg.forEach(function (v) {
            v.style.display="none";
        })
        img[next].style.left="332px";
        animate (img[now],{left:-332},600);
        animate (img[next],{left:0},600);
        // img[now].style.left="-332px";
        // img[next].style.left="0";
        now=next;
        bg[now].style.display="block";
    }
    first.forEach(function (v,i) {
        first[i].onclick=function(){
            bg.forEach(function (v) {
                v.style.display="none";
            })
            if (i==now){
                return;
            } else if (i<now){
                img[i].style.left="-332px";
                animate (img[now],{left:332},600);
                animate (img[i],{left:0},600);
            }else{
                img[i].style.left="332px";
                animate (img[now],{left:-332},600);
                animate (img[i],{left:0},600);
            }
            // animate (img[now],{left:-332},600);
            // animate (img[i],{left:0},600);
            // animate (img[next],{left:332},600);
            bg[i].style.display="block";
            next=now=i;
        }
    })


}