function onClickedAnalysis(){
    console.log("Start to Analyst Plant Leaf");
    var minimumPrice = document.getElementById("uiMinimumPrice");
    var maximumPrice = document.getElementById("uiMaximumPrice");
    var leafImage = document.getElementById("uiImage");
    var predictionResult = document.getElementById("prediction_result");
    var herbalInfo = document.getElementById("herbal_info");
    var herbalmanfaat = document.getElementById("herbal_manfaat");
    var herbalpengolahan = document.getElementById("herbal_pengolahan");
    var recommendationTable = document.getElementById("dataTable");
    var messagebarang = document.getElementById("message_barang");
    var temp = "";
    var idx = 0;

    const point = "http://127.0.0.1:5000/plants_analysis";
    const formData = new FormData();


    formData.append('minimumPrice', parseInt(minimumPrice.value));
    formData.append('maximumPrice', parseInt(maximumPrice.value));
    formData.append('leafImage', leafImage.files[0]);

    fetch(point, {
        method : "post",
        body:formData
    })
    .then(response => response.json())
    .then(data =>{
        predictionResult.innerHTML = "<h2 class='text-result'>"+data.herbal_result.toString()+"</h2>",
        herbalInfo.innerHTML = "<p>"+data.herbal_info.toString()+"</p>",
        herbalmanfaat.innerHTML = "<p>"+data.manfaat_info+"</p>",
        herbalpengolahan.innerHTML = "<p>"+data.pengolahan_info+"</p>",
        data.recommendation.forEach((u)=>{
            idx++;
            temp += "<tr>";
            temp += "<td>"+idx.toString()+"</td>";
            temp += "<td>"+u.nama_daun+"</td>";
            temp += "<td>"+u.harga+"</td>";
            temp += "<td>"+u.butuh+" "+u.satuan+"</td>";
            temp += "<td><a href='"+u.url+"' target='_blank'>"+u.nama_toko+"</a></td>";
            temp += "</tr>";
        })
        recommendationTable.innerHTML = temp,
        messagebarang.innerHTML = "<p>"+data.message+"</p>";

    });
    console.log("done process");
    // console.log(temp);
}

//https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch