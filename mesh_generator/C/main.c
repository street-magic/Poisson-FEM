#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include <stdbool.h>
#include "Node.h" //Nodes and Edges
#define INF DBL_MAX

int main(int argc, char *argv[]) {
	Node node_data; //head is unique
	node_data.x = node_data.y = -INF;
	node_data.next = NULL;

	Edge edge_data; //head of the linked list (unique)
	edge_data.begins_at = edge_data.ends_at = NULL;
	edge_data.next = NULL;

	Edge front; //head of the advancing front datalist
	front.begins_at = front.ends_at = NULL;
	front.prev = front.next = NULL;
	
	FILE *fp = fopen(argv[1], "r");
	int BUFSIZE = 99;
	char buff[BUFSIZE];

	bool python = true;

	Node* first_cont_node = NULL;
	while(fgets(buff, BUFSIZE - 1, fp) != NULL) {
		if (buff[0] != '\n') {
			Node* last_node = &node_data;
			while (last_node->next != NULL) 
				last_node = last_node->next;

			double x, y;
			sscanf(buff, "%lf %lf", &x, &y);
			Node* new_node = add_node(&node_data, x, y);
			if (first_cont_node == NULL){
				first_cont_node = new_node;
			} else {
				add_edge(&edge_data, last_node, new_node);
				add_edge(&front, last_node, new_node);
			}
		} else {
			Node* last_node = first_cont_node;
			while (last_node->next != NULL)
				last_node = last_node->next;
			add_edge(&edge_data, last_node, first_cont_node);
			add_edge(&front, last_node, first_cont_node);
			first_cont_node = NULL;
		}
	}
	fclose(fp);

	double min_angle = 0.1; //? deg
	double max_len = 0.1;
	prepare_initial_front(&front, &edge_data, &node_data, min_angle, max_len);
	Edge* black_box = front.next;
	while(front.next != NULL) {
		advance(&front, &edge_data, &node_data, min_angle, max_len);
	}

	Edge* cur_edge = edge_data.next;
	if (python) {
		printf("import matplotlib.pyplot as plt\n");
		while (cur_edge != NULL) {
			printf("plt.plot([%lf,%lf],",cur_edge->begins_at->x, cur_edge->ends_at->x);
			printf("[%lf,%lf],'.-b')\n",cur_edge->begins_at->y, cur_edge->ends_at->y);
			cur_edge = cur_edge->next;
		}
		cur_edge = black_box;
        /*while (cur_edge != NULL) {
            printf("plt.plot([%lf,%lf],",cur_edge->begins_at->x, cur_edge->ends_at->x);
            printf("[%lf,%lf],'.-r')\n",cur_edge->begins_at->y, cur_edge->ends_at->y);
            cur_edge = cur_edge->next;
        }*/
		printf("plt.axis('equal')\nplt.show()\n");
	}
	return 0;
}
