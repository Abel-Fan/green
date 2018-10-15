window.onload=function () {
    //选项卡
    let lis=document.querySelectorAll(".classify li");
    let a=document.querySelectorAll(".classify li a");
    let all=document.querySelectorAll(".content1 .all");
    let bg=document.querySelector(".bg");
    for (let i=0;i<lis.length;i++){
        lis[i].onclick=function () {
            for (let j=0;j<lis.length;j++){
                all[j].style.display="none";
                a[j].style.color="#aaa";
                lis[j].style.border="1px solid rgba(226,226,226,1)";

            }
            all[i].style.display="block";
            a[i].style.color="#191919";
            lis[i].style.border="1px solid rgba(170,170,170,1)";
            if (i==0) {
                bg.style.height="960px";
            }
            else {
                bg.style.height="621px";
            }
        }
    }
}