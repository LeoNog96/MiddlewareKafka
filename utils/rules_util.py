import re


def is_payload_accept(data, filter_condition):
    if "regx" in filter_condition:
        pass
    else:
        keys_filter = filter_condition.keys()
        status_filter = True
        for k in keys_filter:

            try:
                array_conditons = filter_condition[k]
                if data[k] not in array_conditons:
                    return False

            except Exception:
                continue
        return status_filter


def is_string_value(value):
    first_char_code = ord(value[0])

    last_char_code = ord(value[-1])

    if (first_char_code == 34 or first_char_code == 39) and \
       (last_char_code == 34 or last_char_code == 39):
        return True

    return False


def get_value_string(string_with_quotes :str):

    new_value = string_with_quotes.replace("\"", "")

    new_value = new_value.replace("'", "").strip()

    return new_value


def split_expression(expressao_str):
    regex = r"(?P<VAL1>'.*'|\".*\"|.*)\s\s*(?P<OPERATOR>==|=|>=|<=|!=)\s\s*(?P<VAL2>'.*'|\".*\"|.*)"

    matches = re.findall(regex, expressao_str, re.MULTILINE | re.IGNORECASE)

    if len(matches) == 1:

        val1, operator, val2 = matches[0]

    else:
        raise Exception('Erro ao tentar desestruturar expressao, verifique a sintaxe na expressao: ' + expressao_str)

    return [val1.strip(), operator, val2.strip()]


def process_expression(data, string_expression):

    exp = split_expression(string_expression)

    value_boolean_expression = False

    try:
        val1 = data[exp[0]].strip() if not is_string_value(exp[0]) else get_value_string(exp[0])

        operator = exp[1]

        val2 = data[exp[2]].strip() if not is_string_value(exp[2]) else get_value_string(exp[2])

        value_expression = f'"{val1}" {operator} "{val2}" '

        value_boolean_expression = eval(value_expression)

    except KeyError as ke:

        print('Warning !!!! Nao encontrou o campo no payload, verifique as rules classifications, campo:', ke)
    except Exception as ex:

        print('Erro ao processar expressao: ', str(ex))
    finally:
        return value_boolean_expression


def get_topic_name_by_expressions(data, rule):
    results = []

    name_new_topic = None

    try:

        if 'expression' not in rule or \
           'operator' not in rule or \
           'newTopicName' not in rule:
            raise Exception('Expressao malformada, a mesma deve conter os campos expression, operator e newTopicName')

        expressions_from_rule = rule['expression']

        operator_from_rule = rule['operator']

        for expression in expressions_from_rule:

            res_boolean = process_expression(data, expression)

            results.append(res_boolean)

        if operator_from_rule != 'and' and \
           operator_from_rule != 'or':
            raise Exception('Operador desconhecido, para comparação deve ser informado "and" ou "or" ')

        if operator_from_rule == 'and' and False not in results:

            name_new_topic = rule['newTopicName']

        elif operator_from_rule == 'or' and True in results:

            name_new_topic = rule['newTopicName']

    except Exception as e:
        print('Erro ao classificar topico, erro: ', str(e))

    return name_new_topic


def classification_data(data, topic_rules):
    topic_default_name = 'not_classified'

    if "defaultNameNewTopic" in topic_rules:
        topic_default_name = topic_rules["defaultNameNewTopic"]

    rules = topic_rules['rules']

    new_topic_name = ''
    for rule in rules:

        try:
            new_topic_name = get_topic_name_by_expressions(data, rule)

            if new_topic_name is not None:
                break

        except Exception as ex:
            print('Erro ao classificar dados ' + str(ex))

    return new_topic_name if new_topic_name is not None else topic_default_name


def model_map_util(map_model, data):
    """
    Metodo recursivo de map apartir de um modelo já definido
    Args:
        map_model: dict com o modelo desejado, com os valores sendo qual dados desejam
        data: payload com os dados brutos

    Returns:
        dict modelado da forma especificada
    """
    for k, v in map_model.items():
        if isinstance(v, dict):
            map_model[k] = model_map_util(v, data)
        elif isinstance(v, list):
            map_model[k] = []
            for x in v:
                map_model[k].append(model_map_util(x, data))
        else:
            try:
                if is_string_value(v):
                    map_model[k] = get_value_string(v)
                else:
                    map_model[k] = get_values(v.split('.'), data)
            except AttributeError:
                map_model[k] = v
            except TypeError:
                map_model[k] = v

    return map_model


def get_values(string, dictionary):
    """
    Metodo para pegar valores de um dict indepedente da hierarquia em que se encontra
    Args:
        string: nivel desejado. ex: teste.objeto.id
        dictionary: dict que contem o valor desejado

    Returns:
        Retorna o valor da chave especificada
    """
    new_dictionary = dictionary

    for x in string:
        new_dictionary = new_dictionary.get(x)

    return new_dictionary

# "map_model": {
#     "issue": {
#         "id": None,
#         "project_id": 146,
#         "subject": "name",
#         "priority_id": 29,
#         "description": "descrption",
#         "tracker_id": 7,
#         "is_private": True,
#         "custom_fields": [
#             {
#                 "id": 83,
#                 "value": "number"
#             }
#         ],
#         "status_id": 1
#     }
# }

# t = {
#     'payload':{
#         'name':'teste2',
#         'number':  88,
#         'descrption':'teste3',
#         'updated_at': '2020-02-05T00:00',
#         'created_at': '2020-02-05T00:00',
#         'card_type_name': 'Story'
#     }
# }