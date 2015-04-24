$(function(){$('#Preguntar').on('click',function(evt){evt.preventDefault();
var pregunta=$('#Pregunta').val();
$.ajax({url:"/tutor/alternative/",
data:{"question":pregunta},
cache:false,
success:function(data){
	if(data.exito){
		if(data.alternativa){
			// Preguntar si se refiere a la pregunta alternativa TODO insertar alternativa al html
			$.blockUI({ message:$('#question'), css: { width: '350px' }})
			$('#yes').click(function() {
					$.unblockUI()
					$('#Pregunta').html(data.alternativa);
					$('#Respuesta').html(data.respuesta_alt);
				});
			$('#no').click(function() {
					$.unblockUI()
					//$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
					$.ajax({url:"/tutor/question/",
					data:{"question":pregunta},
					cache:false,
					success:function(data){
						if(data.exito){				
						$('#Respuesta').html(data.respuesta);
						}else{
								$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
					}},crossDomain:false,type:"POST",dataType:"json",error:function(jqXHR,textStatus,errorThrown){alert(errorThrown);}});
					
				});	
		}else{
			$.ajax({url:"/tutor/question/",
				data:{"question":pregunta},
				cache:false,
				success:function(data){
					if(data.exito){				
					$('#Respuesta').html(data.respuesta);
					}else{
							$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
				}},crossDomain:false,type:"POST",dataType:"json",error:function(jqXHR,textStatus,errorThrown){alert(errorThrown);}});		
		
		}
		
	}else{$('#Respuesta').html("<font color=\"red\">No se pudo procesar la pregunta</font>");/*
		$.blockUI({ message:$('#question'), css: { width: '275px' }})
		$('#yes').click(function() {
				$.unblockUI()
				//$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
				$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
			});
		$('#no').click(function() {
				$.unblockUI()
				//$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
				$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
	*************************************** 
				$.ajax({url:"/tutor/question/",
				data:{"question":pregunta},
				cache:false,
				success:function(data){
					if(data.exito){				
					$('#Respuesta').html(data.respuesta);
					}else{
							$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
				}},crossDomain:false,type:"POST",dataType:"json",error:function(jqXHR,textStatus,errorThrown){alert(errorThrown);}});
	***************************************			
				
			});		
		//$('#Respuesta').html("<font color=\"red\">No se encontró la respuesta</font>");
		*/
}},crossDomain:false,type:"POST",dataType:"json",error:function(jqXHR,textStatus,errorThrown){alert(errorThrown);}});});});


// if si, guardar la pregunta con el texto actual
// if no, llamar funcion que busca en el grafo

//$("#input-22").rating();
/* Initialize your rating via javascript as follows */
$("#input-22").rating({
    starCaptions: {1: "Poor", 2: "Bad", 3: "Ok", 4: "Good", 5: "Excelent"},
    //starCaptionClasses: {1: "text-danger", 2: "text-warning", 3: "text-info", 4: "text-primary", 5: "text-success"},
});

//$(document).ajaxStart($.blockUI).ajaxStop($.unblockUI); #6f7a9f


$(document).ready(function () {
	$('#Pregunta').html("otra pregunta");
	
    $(document).ajaxStart(function () {
		
		$('#tutor-content').block({ message: '<h1><img src="'+static_url+'images/loading.gif" /> <font color="blue" size="3px">Please wait for your Answer</font> </h1>' });
        //$("#loading").show();
    }).ajaxStop(function () {
		$('#tutor-content').unblock()
        //$("#loading").hide();
    });
});