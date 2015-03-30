$(function(){
			
	$('#Preguntar').on('click',function(evt){
		evt.preventDefault();
		var pregunta = $('#Pregunta').val();
		//alert(pregunta);
		$.ajax({
			url: "/tutor/question/",
			data: {"question":pregunta},
			cache: false,
			success: function(data) {
				if (data.exito){
					$('#Respuesta').html(data.respuesta);
				}
				else{
					$('#Respuesta').html("<font color=\"red\">No se encontr� la respuesta</font>");
				}
				
			},
			crossDomain: false,
			type: "POST",
			dataType: "json",
			error:function(jqXHR, textStatus, errorThrown) {
				alert(errorThrown);
			}
		});
		
	});



});