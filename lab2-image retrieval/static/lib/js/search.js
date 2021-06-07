
function myFunction(){
	document.getElementById("predictedResult").innerHTML= "";
	//$('#clear').hide();
}

function myRandom(res){
	length=res.length
	var arr=[]
	for (var i=0;i<length;i++){
		arr.push(i)
	}
	arr.sort(function(){
		0.5-Math.random()
	})
	console.log("打乱后的arr",arr)
	arr.length=9
	return arr
}

function search(){
	console.log("点击search");
	var file=$("#file").val()

	if(!file){
		alert("表单为空")
	return
	}

	//搜索前重置fav
	for(var i=0;i<9;i++){
		document.getElementById("img-div"+i).src='/lib/img/unfav.png' ;
	}

	


	document.getElementById("load").style.display="block";
	console.log("加载gif")

	$("form").submit(function(evt){
			console.log("表单函数")
	evt.preventDefault();
	var formData = new FormData($(this)[0]);

	$.ajax({
			url: 'imgUpload',
		type: 'POST',
			data: formData,
			//async: false,
			cache: false,
			contentType: false,
			enctype: 'multipart/form-data',
			processData: false,

			success: function (response) {

		
		
				document.getElementById("load").style.display="none";
				console.log("隐藏gif")

				var k=18 //显示9张图片
				var tagSets=new Set(); //tag集合


                 document.getElementById("img0").src = response.image0[0];
				 document.getElementById("img0").name=response.image0[1];
				 tagSets.add(response.image0[1]);
				 

		 		document.getElementById("img1").src = response.image1[0];
				 document.getElementById("img1").name = response.image1[1];
				 tagSets.add(response.image1[1]);


                document.getElementById("img2").src = response.image2[0];
				document.getElementById("img2").name = response.image2[1];
				tagSets.add(response.image2[1]);


                document.getElementById("img3").src = response.image3[0];
				document.getElementById("img3").name = response.image3[1];
				tagSets.add(response.image3[1]);

                 document.getElementById("img4").src = response.image4[0];
				 document.getElementById("img4").name = response.image4[1];
				 tagSets.add(response.image4[1]);

                 document.getElementById("img5").src = response.image5[0];
				 document.getElementById("img5").name = response.image5[1];
				 tagSets.add(response.image5[1]);

                 document.getElementById("img6").src = response.image6[0];
				 document.getElementById("img6").name = response.image6[1];
				 tagSets.add(response.image6[1]);


                 document.getElementById("img7").src = response.image7[0];
				 document.getElementById("img7").name = response.image7[1];
				 tagSets.add(response.image7[1]);


                 document.getElementById("img8").src = response.image8[0];
				 document.getElementById("img8").name = response.image8[1];
				 tagSets.add(response.image8[1]);

				 //document.getElementById("uploadedImages").src=response.uploaded;
				 document.getElementById("uploadedImages").style.display="block";
				 document.getElementById("review").style.display="block";



				 //@TODO document.getElementById("uploadedImages").src=response.uploaded;
				 document.getElementById("labels").style.display="block";

				 for(var i=0;i<9;i++){
					document.getElementById("img-div"+i).style.display="block";
				}
				 var it=tagSets.values();
				 for(var i=0;i<tagSets.size;i++){
					 var idName='tag'+i;
					 document.getElementById(idName).textContent=it.next().value;
					 document.getElementById(idName).style.display="block";
				 }
				 document.getElementById("tag").textContent="all";
				 document.getElementById("tag").style.display="block";

				 for(let i=0;i<9;i++){
					document.getElementById("img_tag"+i).textContent=document.getElementById("img"+i).name;
					// document.getElementById("img_tag"+i).style.display="block";
				 }

				 //@TODO document.getElementById("uploaded").style.display="block";
				 
				 console.log("加载图片完毕！")
		   //$('#clear').show();


			}
	});
	});
}	   
   		