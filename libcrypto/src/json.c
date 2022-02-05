#include <stddef.h>
#include <stdbool.h>
#include "include/json.h"

struct json_token *json_alloc_token(struct json_parser *parser, struct json_token *tokens, const size_t num_tokens)
{
	struct json_token *token;
	if(parser->tok_next >= num_tokens)
	{
		return NULL;
	}
	token = &tokens[parser->tok_next++];
	token->start = token->end = -1;
	token->size = 0;
	#ifdef JSON_PARENT_LINKS
	token->parent = -1;
	#endif
	return token;
}

void json_fill_token(struct json_token *token, const json_type_t type, const int start, const int end)
{
	token->type = type;
	token->start = start;
	token->end = end;
	token->size = 0;
}

//Fill next token with JSON primative
int json_parse_primitive(struct json_parser *parser, const char *json, const size_t len, struct json_token *tokens, const size_t num_tokens)
{
	struct json_token *token;
	int start = parser->pos;
	bool last_took_default_path = false;
	bool break_loop = false;
	for(; parser->pos < len && json[parser->pos] != '\0'; parser->pos++)
	{
		switch(json[parser->pos])
		{
			#ifndef JSON_STRICT
			case ':':
			#endif
			case '\t':
			case '\r':
			case '\n':
			case ' ':
			case ',':
			case ']':
			case '}':
				break_loop = true;
				last_took_default_path = false;
				break;
			default:
				if(json[parser->pos] < 32 || json[parser->pos] >= 127)
				{
					parser->pos = start;
					return JSON_ERROR_INVALID;
				}
				break_loop = false;
				last_took_default_path = true;
				break;
		}
		if(break_loop)
		{
			break;
		}
	}
	
	if(last_took_default_path)
	{
		#ifdef JSON_STRICT
		parser->pos = start;
		return JSON_ERROR_PARTIAL;
		#endif
	}
	
	if(tokens == NULL)
	{
		parser->pos--;
		return 0;
	}
	token = json_alloc_token(parser, tokens, num_tokens);
	if(token == NULL)
	{
		parser->pos = start;
		return JSON_ERROR_NOMEM;
	}
	json_fill_token(token, JSON_PRIMITIVE, start, parser->pos);
	#ifdef JSON_PARENT_LINKS
	token->parent = parser->tok_super;
	#endif
	parser->pos--;
	return 0;
}

int json_parse_string(struct json_parser *parser, const char *json, const size_t len, struct json_token *tokens, const size_t num_tokens)
{
	struct json_token *token;
	int start = parser->pos;
	parser->pos++; //Skip starting quote
	
	for(; parser->pos < len && json[parser->pos] != '\0'; parser->pos++)
	{
		char c = json[parser->pos];
		if(c == '\"')
		{
			if(tokens == NULL){return 0;}
			token = json_alloc_token(parser, tokens, num_tokens);
			if(token == NULL)
			{
				parser->pos = start;
				return JSON_ERROR_NOMEM;
			}
			json_fill_token(token, JSON_STRING, start+1, parser->pos);
			#ifdef JSON_PARENT_LINKS
			token->parent = parser->tok_super;
			#endif
			return 0;
		}
		if(c == '\\' && parser->pos+1 < len)
		{
			parser->pos++;
			switch(json[parser->pos])
			{
				case '\"':
				case '/':
				case '\\':
				case 'b':
				case 'f':
				case 'r':
				case 'n':
				case 't':
					break;
				case 'u':
					parser->pos++;
					for(int i = 0; i < 4 && parser->pos < len && json[parser->pos] != '\0'; i++)
					{
						if(!((json[parser->pos] >= 48 && json[parser->pos] <= 57) ||   /* 0-9 */
							(json[parser->pos] >= 65 && json[parser->pos] <= 70) ||   /* A-F */
							(json[parser->pos] >= 97 && json[parser->pos] <= 102)))  /* a-f */
						{
							parser->pos = start;
							return JSON_ERROR_INVALID;
						}
						parser->pos++;
					}
					parser->pos--;
					break;
				default:
					parser->pos = start;
					return JSON_ERROR_INVALID;
			}
		}
	}
	parser->pos = start;
	return JSON_ERROR_PARTIAL;
}

int json_parse(struct json_parser *parser, const char *json, const size_t len, struct json_token *tokens, const unsigned int num_tokens)
{
	int r, i;
	struct json_token *token;
	int count = parser->tok_next;
	
	for(; parser->pos < len && json[parser->pos] != '\0'; parser->pos++)
	{
		char c = json[parser->pos];
		json_type_t type;
		
		switch(c)
		{
			case '{':
			case '[':
				count++;
				if(tokens == NULL)
				{
					break;
				}
				token = json_alloc_token(parser, tokens, num_tokens);
				if(token == NULL)
				{
					return JSON_ERROR_NOMEM;
				}
				if(parser->tok_super != -1)
				{
					struct json_token *t = &tokens[parser->tok_super];
					#ifdef JSON_STRICT
					if(t->type == JSON_OBJECT)
					{
						return JSON_ERROR_INVALID;
					}
					#endif
					t->size++;
					#ifdef JSON_PARENT_LINKS
					token->parent = parser->tok_super;
					#endif
				}
				token->type = (c == '{' ? JSON_OBJECT : JSON_ARRAY);
				token->start = parser->pos;
				parser->tok_super = parser->tok_next - 1;
				break;
			case '}':
			case ']':
				if(tokens == NULL)
				{
					break;
				}
				type = (c == '}' ? JSON_OBJECT : JSON_ARRAY);
				#ifdef JSON_PARENT_LINKS
				if(parser->tok_next < 1)
				{
					return JSON_ERROR_INVALID;
				}
				token = &tokens[parser->tok_next - 1];
				for(;;)
				{
					if(token->start != -1 && token->end == -1)
					{
						if(token->type != type)
						{
							return JSON_ERROR_INVALID;
						}
						token->end = parser->pos + 1;
						parser->tok_super = token->parent;
						break;
					}
					if(token->parent == -1)
					{
						if(token->type != type || parser->tok_super == -1)
						{
							return JSON_ERROR_INVALID;
						}
						break;
					}
					token = &tokens[token->parent];
				}
				#else
				for(i = parser->tok_next - 1; i >= 0; i--)
				{
					token = &tokens[i];
					if(token->start != -1 && token->end == -1)
					{
						if (token->type != type)
						{
							return JSON_ERROR_INVALID;
						}
						parser->tok_super = -1;
						token->end = parser->pos + 1;
						break;
					}
				}
				if(i == -1)
				{
					return JSON_ERROR_INVALID;
				}
				for(; i >= 0; i--)
				{
					token = &tokens[i];
					if(token->start != -1 && token->end == -1)
					{
						parser->tok_super = i;
						break;
					}
				}
				#endif
				break;
			case '\"':
				r = json_parse_string(parser, json, len, tokens, num_tokens);
				if(r < 0)
				{
					return r;
				}
				count++;
				if(parser->tok_super != -1 && tokens != NULL)
				{
					tokens[parser->tok_super].size++;
				}
				break;
			case '\t':
			case '\r':
			case '\n':
			case ' ':
				break;
			case ':':
				parser->tok_super = parser->tok_next - 1;
				break;
			case ',':
				if(tokens != NULL && parser->tok_super != -1 &&
					tokens[parser->tok_super].type != JSON_ARRAY &&
					tokens[parser->tok_super].type != JSON_OBJECT)
				{
					#ifdef JSON_PARENT_LINKS
					parser->tok_super = tokens[parser->tok_super].parent;
					#else
					for(i = parser->tok_next - 1; i >= 0; i--)
					{
						if(tokens[i].type == JSON_ARRAY || tokens[i].type == JSON_OBJECT)
						{
							if(tokens[i].start != -1 && tokens[i].end != -1)
							{
								parser->tok_super = i;
								break;
							}
						}
					}
					#endif
				}
				break;
			#ifdef JSON_STRICT
			case '-':
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
			case 't':
			case 'f':
			case 'n':
				if(tokens != NULL && parser->tok_super != -1)
				{
					const struct json_token *t = &tokens[parser->tok_super];
					if(t->type == JSON_OBJECT || (t->type == JSON_STRING && t->size != 0))
					{
						return JSON_ERROR_INVALID;
					}
				}
			#else
			default:
			#endif
				r = json_parse_primitive(parser, json, len, tokens, num_tokens);
				if(r < 0)
				{
					return r;
				}
				count++;
				if(parser->tok_super != -1 && tokens != NULL)
				{
					tokens[parser->tok_super].size++;
				}
				break;
			#ifdef JSON_STRICT
			default:
				return JSON_ERROR_INVALID;
			#endif
		}
	}
	if(tokens != NULL)
	{
		for(i = parser->tok_next - 1; i >= 0; i--)
		{
			if(tokens[i].start != -1 && tokens[i].end == -1)
			{
				return JSON_ERROR_PARTIAL;
			}
		}
	}
	return count;
}

void json_init(struct json_parser *parser)
{
	parser->pos = 0;
	parser->tok_next = 0;
	parser->tok_super = -1;
}
