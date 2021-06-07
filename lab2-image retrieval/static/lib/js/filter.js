
function filter(obj){
    var tagID=obj.id
    var tagName=document.getElementById(tagID).textContent

    for(var i=0;i<9;i++){
        document.getElementById("img-div"+i).style.display="block";
    }

    if(tagName!="all"){
        for(var i=0;i<9;i++){
            var curId="img"+i;
            if(document.getElementById(curId).name!=tagName){
                document.getElementById("img-div"+i).style.display="none";
            }
        }
    }
}

