#ifndef _NODE_H_
#define _NODE_H_

#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

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

Node* node_push_back (Node* node_list, Node* new_node) {
	Node* cur_node = node_list;
	while (cur_node->next != NULL) {
		cur_node = cur_node->next;
	}
	cur_node->next = new_node;
	return new_node;
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
	struct Edge* prev;
	struct Edge* next;
};
typedef struct Edge Edge;

void draw_edge(Edge* cur_edge){
    printf("plt.plot([%lf,%lf],",cur_edge->begins_at->x, cur_edge->ends_at->x);
    printf("[%lf,%lf],'.-b')\n",cur_edge->begins_at->y, cur_edge->ends_at->y);
}

Edge* create_edge (Node* start, Node* finish) {
		struct Edge* ret_edge = malloc(sizeof(struct Edge));
		if (ret_edge == NULL)
				return NULL;
		ret_edge->prev = NULL;
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
		new_edge->prev = cur_edge;
	return new_edge;
}

void remove_edge (Edge* edge) {
	edge->prev->next = edge->next;
	if (edge->next != NULL)
		edge->next->prev = edge->prev;
	free(edge);
}

double len (Edge* edge) {
	double x1 = edge->begins_at->x;
	double y1 = edge->begins_at->y;
	double x2 = edge->ends_at->x;
	double y2 = edge->ends_at->y;
	return sqrt(pow(x2-x1, 2.0) + pow(y2-y1, 2.0));
}

double len_nodes (Node* a, Node* b) {
	double x1 = a->x;
	double y1 = a->y;
	double x2 = b->x;
	double y2 = b->y;
	return sqrt(pow(x2-x1, 2.0) + pow(y2-y1, 2.0));
}

Node* create_mid_node (Edge* edge) {
	double x1 = edge->begins_at->x;
	double y1 = edge->begins_at->y;
	double x2 = edge->ends_at->x;
	double y2 = edge->ends_at->y;
	Node* new_node = create_node((x1+x2)/2.0, (y1+y2)/2.0);
	return new_node;
}

void divide_edge (Edge* div_edge, Edge* front, Edge* edges, Node* nodes) {
	Node* mid_node = create_mid_node (div_edge);
	node_push_back(nodes, mid_node);
	Edge* cur_edge = edges->next;
	while (cur_edge != NULL) {
		if (cur_edge->begins_at == div_edge->begins_at && cur_edge->ends_at == div_edge->ends_at) {
			add_edge(front, div_edge->begins_at, mid_node);
			add_edge(front, mid_node, div_edge->ends_at);
			remove_edge(div_edge);

			add_edge(edges, cur_edge->begins_at, mid_node);
			add_edge(edges, mid_node, cur_edge->ends_at);
			remove_edge(cur_edge);
			break;
		}
		cur_edge = cur_edge->next;
	}
}

void prepare_initial_front (Edge* front, Edge* edges, Node* nodes, double min_angle, double max_len) {
	bool is_prepared = false;
	while (is_prepared == false) {
		is_prepared = true;
		Edge* cur_front = front->next;
		while (cur_front != NULL) {
			Edge* next = cur_front->next;
			double l = len(cur_front);
			if(l > max_len) {
				is_prepared = false;
				divide_edge(cur_front, front, edges, nodes);
			}
			cur_front = next;
		}
	}
}

Node* create_ideal_node(Edge* edge) {
	double x1 = edge->begins_at->x;
	double y1 = edge->begins_at->y;
	double x2 = edge->ends_at->x;
	double y2 = edge->ends_at->y;
	
	double new_x = (x1 + x2)/2 - 0.866*(y2 - y1); //0.866
	double new_y = (y1 + y2)/2 + 0.866*(x2 - x1);
	Node* new_node = create_node(new_x, new_y);
	return new_node;
}

double cross(Node* A, Node* B, Node* C) {
	double a = A->x - C->x;
	double b = A->y - C->y;
	double c = B->x - C->x;
	double d = B->y - C->y;
	return a*d - b*c;
}

double d(Node* A, Node* B, Node* C) {
	double prod = cross(A, B, C);
	if (prod > 0.0)
		return 1.0;
	if (prod < 0.0)
		return -1.0;
	return 0.0;
}

bool intersect(Edge* AB, Node* C, Edge* UV) {
	Node* A = AB->begins_at;
	Node* B = AB->ends_at;
	Node* U = UV->begins_at;
	Node* V = UV->ends_at;
	int common_nodes = 0;
	if (U == A || U == B || U == C)
		common_nodes++;
	if (V == A || V == B || V == C)
		common_nodes++;
	if (common_nodes == 0) {
		if ( ((d(U,V,A) + d(U,V,B) + d(U,V,C)) == 3) ||
			 ((d(U,V,A) + d(U,V,B) + d(U,V,C)) == -3)||
			 ((d(A,B,U) + d(A,B,V)) == -2) ||
			 ((d(B,C,U) + d(B,C,V)) == -2) ||
			 ((d(C,A,U) + d(C,A,V)) == -2))
		{
			return false;
		}
	}
	if (common_nodes == 1) {
		if ( ((d(A,B,U) + d(A,B,V)) == -1) ||
			 ((d(B,C,U) + d(B,C,V)) == -1) ||
			 ((d(C,A,U) + d(C,A,V)) == -1))
		{
			return false;
		}
	}
	if (common_nodes == 2) {
		return false;
	}
	return true;
}

bool is_acceptable(Edge* chosen_edge, Node* candidate_node, Edge* front, double min_angle, double max_len) {
	if (d(chosen_edge->begins_at, chosen_edge->ends_at, candidate_node) < 0) {
		return false;
	}
	
	Edge* cur_front = front->next;
	while (cur_front != NULL) {
		if (intersect(chosen_edge, candidate_node, cur_front)) {
            /*printf("# UNWANTED INTERSECTION\n");
            draw_edge(chosen_edge);
            draw_edge(cur_front);
            draw_edge(create_edge(chosen_edge->begins_at, candidate_node));
            draw_edge(create_edge(candidate_node, chosen_edge->ends_at));*/

			return false;
		}
		cur_front = cur_front->next;
	}
	
	return true;
}

void advance (Edge* front, Edge* edges, Node* nodes, double min_angle, double max_len) {
	// front is never empty [ HEAD -> NULL ]
	double min_len = len(front->next);
	Edge* min_front = front->next;
	Edge* cur_front = front->next->next;
	while (cur_front != NULL) {
		double l = len(cur_front);
		if(l < min_len) {
			min_len = l;
			min_front = cur_front;
		}
		cur_front = cur_front->next;
	} //found min_front

	double alpha = 0.5;
	Node* ideal_node = create_ideal_node(min_front);
	Node* best_node = NULL;
	min_len = 1000000000;
	bool is_new = false;

    cur_front = front->next;
	while (cur_front != NULL) {
		Node* candidate_node = cur_front->begins_at;
		double new_len = len_nodes(ideal_node, candidate_node);
		if ((candidate_node != min_front->begins_at && candidate_node != min_front->ends_at) &&
			(new_len < max_len*alpha) &&
			is_acceptable(min_front, candidate_node, front, min_angle, max_len))
		{
			if (new_len < min_len) {
				best_node = candidate_node;
				min_len = new_len;
			}
		}
		cur_front = cur_front->next;
	}

	if (best_node == NULL && is_acceptable(min_front, ideal_node, front, min_angle, max_len)) {
	    best_node = ideal_node;
	    is_new = true;
	}
	
	if (best_node == NULL) {
	    printf("# FAILED TO ADVANCE THE FRONT\n");
		front->next = NULL;
		return;
	}
	if (is_new) {
		node_push_back(nodes, best_node);
		add_edge(edges, min_front->begins_at, best_node);
		add_edge(edges, best_node, min_front->ends_at);
		
		add_edge(front, min_front->begins_at, best_node);
		add_edge(front, best_node, min_front->ends_at);
		remove_edge(min_front);
	} else {
		free(ideal_node);
		bool add_left = true;
		bool add_right = true;
		cur_front = front->next;
		while (cur_front != NULL) {
			if (cur_front->begins_at == min_front->ends_at && cur_front->ends_at == best_node) {
				remove_edge(cur_front);
				add_right = false;
			}
			if (cur_front->begins_at == best_node && cur_front->ends_at == min_front->begins_at) {
				remove_edge(cur_front);
				add_left = false;
			}
			cur_front = cur_front->next;
		}
		if (add_right) {
            cur_front = edges->next;
            add_edge(front, best_node, min_front->ends_at);
            bool add_edge_right = true;
            while (cur_front != NULL) {
                if ((cur_front->begins_at == min_front->ends_at && cur_front->ends_at == best_node) ||
                    (cur_front->ends_at == min_front->ends_at && cur_front->begins_at == best_node)) {
                    add_edge_right = false;
                    break;
                }
                cur_front = cur_front->next;
            }
            if(add_edge_right)
                add_edge(edges, best_node, min_front->ends_at);
        }
		if (add_left) {
            cur_front = edges->next;
			add_edge(front, min_front->begins_at, best_node);
			bool add_edge_left = true;
            while (cur_front != NULL) {
                if ((cur_front->begins_at == min_front->begins_at && cur_front->ends_at == best_node) ||
                    (cur_front->ends_at == min_front->begins_at && cur_front->begins_at == best_node)) {
                    add_edge_left = false;
                }
                cur_front = cur_front->next;
			}
            if(add_edge_left)
                add_edge(edges, min_front->begins_at, best_node);
		}
		remove_edge(min_front);
	}
}
#endif