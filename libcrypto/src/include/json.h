#ifndef JSON_H
#define JSON_H

#include <stddef.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define JSON_STRICT
#define JSON_PARENT_LINKS

typedef enum
{
	JSON_UNDEFINED	= 0,
	JSON_OBJECT		= 1 << 0,
	JSON_ARRAY		= 1 << 1,
	JSON_STRING		= 1 << 2,
	JSON_PRIMITIVE	= 1 << 3
} json_type_t;

enum json_err
{
	JSON_ERROR_NOMEM = -1, //Not enough tokens provided
	JSON_ERROR_INVALID = -2, //Invalid character
	JSON_ERROR_PARTIAL = -3 //Partial json more bytes expected
};

struct json_token
{
	json_type_t type;
	int start;
	int end;
	int size;
	#ifdef JSON_PARENT_LINKS
	int parent;
	#endif
};

struct json_parser
{
	unsigned int pos; //JSON str offset
	unsigned int tok_next; //Next token
	int tok_super; //Parent node or array
};

void json_init(struct json_parser *parser);
int json_parse(struct json_parser *parser, const char *json, const size_t len, struct json_token *tokens, const unsigned int num_tokens);

#ifdef __cplusplus
}
#endif

#endif
