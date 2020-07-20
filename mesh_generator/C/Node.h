#include <stdlib.h>
struct Node {
	double x, y;
	struct Node* next;
};
typedef struct Node Node;

struct Node* create_node (double new_x, double new_y) {
	struct Node* ret_node = malloc(sizeof(struct Node));
	if (ret_node == NULL)
		return NULL;
	ret_node->next = NULL;
	ret_node->x = new_x;
	ret_node->y = new_y;

	return ret_node;
}

Node* add_node (Node* node_list, double x, double y) {
	Node* cur_node = node_list;
	while (cur_node->next != NULL) {
		cur_node = cur_node->next;
	}
	Node* new_node = create_node(x, y);
	cur_node->next = new_node;
	return new_node;
}

struct Edge {
	Node* begins_at;
	Node* ends_at;
	struct Edge* next;
};
typedef struct Edge Edge;

Edge* create_edge (Node* start, Node* finish) {
        struct Edge* ret_edge = malloc(sizeof(struct Edge));
        if (ret_edge == NULL)
                return NULL;
        ret_edge->next = NULL;
        ret_edge->begins_at = start;
        ret_edge->ends_at = finish;

        return ret_edge;
}

Edge* add_edge (Edge* edge_list, Node* start, Node* finish) {
	Edge* cur_edge = edge_list;
        while (cur_edge->next != NULL) {
                cur_edge = cur_edge->next;
        }
        Edge* new_edge = create_edge(start, finish);
        cur_edge->next = new_edge;
	return new_edge;
}
