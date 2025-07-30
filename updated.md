Principais Alterações

# Customers

Agora atende pessoa física e pessoa jurídica, segue as alterações nos endpoints

## Create Customer
Estrutura da requisição
{
    "customer_type": "", // PF ou PJ
    "document": "", // CPF ou CNPJ
    "name": "",
    "fantasy_name": "", // Não obrigatório
    "phone_number": "",
    "email": "", // Não obrigatório
    "birth_date": null, // Não obrigatório
    "contact": {
        "name": "",
        "date_of_birth": "",
        "contact_phone": "",
        "contact_email": ""
    }, // Não obrigatório para PF, inserir flag "Utilizar contato padrão" no frontend quando for PF. (Campo "Email" passa a ser obrigatório)
    "billing_address": {
        "cep": "",
        "street_name": "",
        "district": "",
        "number": "",
        "city": "",
        "state": ""
    }
}

no caso de pessoa física, quando não informado o campo birth_date, enviar como null

## Update Customer
Alterado de PATCH para PUT, precisa que todas as informações do cliente sejam informadas na requisição, alteradas ou não.

Estrutura da requisição
{
    "id": "",
    "customer_type": "",
    "document": "",
    "name": "",
    "fantasy_name": "",
    "phone_number": "",
    "email": "",
    "birth_date": null,
    "state_registration": "",
    "contact": {
        "name": "",
        "date_of_birth": "",
        "contact_phone": "",
        "contact_email": ""
    },
    "billing_address": {
        "cep": "",
        "street_name": "",
        "district": "",
        "number": "",
        "city": "",
        "state": ""
    }
}

# Products

Configuração de produção diária removida e aplicada técnica soft delete na exclusão de produtos, onde ao invés de excluir, apenas marcamos como inativo, segue as alterações nos endpoints

## Create Product
Estrutura da requisição
{
    "name": "",
    "price": "9.99",
    "weight": "0.00",
    "current_stock": 0
}

## Update Product
Alterado de PATCH para PUT, precisa que todas as informações do produto sejam informadas na requisição, alteradas ou não.

Estrutura da requisição
{
    "id": "",
    "name": "",
    "price": "",
    "weight": "",
    "current_stock": 0
}

## Delete Product
Não excluir o produto diretamente do banco, apenas marca como inativo.

## Get List Products
Agora funciona através de filtros por status, na página de produtos deve aparecer apenas os produtos ativos, com opções de filtro para listar todos os produtos ou apenas os produtos inativos.

Opções de filtro:
1 - active
2 - inactive
3 - all

Estrutura da url:
{{host}}/api/products/?list&status=active&page=1&page_size=100

# Order 

Campo adicionado para definir o método de entrega, podendo ser: "RETIRADA" ou "ENTREGUE". Adicionar campo nos endpoints Create e Update, estrutura e métodos seguem os mesmos.

# Order Status

Definidos com base no método de entrega, segue as alterações nos endpoints.

## Get List Status

Parâmetro adicionado para filtrar os status com base no método de entrega do pedido.

Opções de filtro:
1. "ENTREGA"
2. "RETIRADA"

Estrutura da url:
{{host}}/api/orders/status/?delivery_method=

Retorna os status genéricos como "Aguardo do expediente", "Em separação", "Aguardando pagamento", "Concluído" e os status específicos para cada método de entrega.

Todas os endpoints estão atualizados e documentados no postman.