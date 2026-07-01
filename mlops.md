  La columna "Atención" hace referencia al mecanismo de atención de la arquitectura del        
  transformador del modelo:                                                                    
                                                                                               
  • MHA (Multi-Head Attention): La atención clásica. Consume una cantidad enorme de memoria    
  caché (KV Cache) por usuario.                                                                
  • GQA (Grouped-Query Attention): Usado por Llama 3, Mistral y la mayoría de modelos modernos.
  Reduce el consumo de caché en unas 8 veces.                                                  
  • MLA (Multi-Head Latent Attention): Introducido por DeepSeek. Comprime la memoria del caché 
  de forma masiva, reduciendo su tamaño en más de un 90%.                                      
                                                         