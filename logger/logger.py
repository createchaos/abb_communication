'''
. . . . . . . . . . . . . . . . . . 
.                                 .
.   <<><><>    <<><><>  <<        .
.   <<    ><   <<       <<        .
.   <<><><>    <<><><   <<        .  
.   <<  ><     <<       <<        .
.   <<   <>    <<       <<        .
.   <<    ><   <<       <<><><>   .
.                                 .
.             GKR 2016/17         .
. . . . . . . . . . . . . . . . . .

Created on 09.12.2016

@author: kathrind, stefanap 
'''

import pickle
import os

class Logger:
    
    def __init__(self, filename_pkl = "\output_nodes.pkl", filename_txt = "\log_nodes.txt", logpath = os.path.dirname(__file__) + "\log_files"):
        self.path_nodes_built =  logpath + filename_pkl
        self.path_nodes_built_txt = logpath + filename_txt
        
    def restore_files(self):
        self.output_nodes_built = open(self.path_nodes_built, 'a')
        self.log_nodes_built = open(self.path_nodes_built_txt, 'a')
    
    def delete_files(self):
        self.output_nodes_built = open(self.path_nodes_built, 'w')
        self.log_nodes_built = open(self.path_nodes_built_txt, 'w')
    
    def open_files(self):
        self.output_nodes_built = open(self.path_nodes_built, 'a')
        self.log_nodes_built = open(self.path_nodes_built_txt, 'a')
    
    def close_files(self):
        self.log_nodes_built.close()
        self.output_nodes_built.close()
    
    def log_node(self, idx_node):
        self.open_files()
        self.pickle_node(idx_node)
        self.write_node(idx_node)
        self.close_files()
        
    def pickle_node(self, idx_node):
        node_idx_dict = {i: [idx_node][i] for i in range(0, len([idx_node]))}
        pickle.dump(node_idx_dict, self.output_nodes_built)
    
    def write_node(self, idx_node):
        self.log_nodes_built.write(str(idx_node)+ "\n")
    
    def get_built_nodes(self):
        pkl_file = open(self.path_nodes_built, 'rb')

        nodes_built_list = []
        ok = True
        while ok:
            try:
                node_idx = pickle.load(pkl_file)
                nodes_built_list.append(node_idx.values()[0])        
            except:
                ok = False
        pkl_file.close()
        
        #return list(set(nodes_built_list))
        return list(nodes_built_list)
    
    def reset_from_logfile(self, nodes):        
        idx_list = self.get_built_nodes()
        for idx in idx_list:
            nodes[idx].is_built = True



if __name__ == '__main__':
    logger = Logger()
    """
    logger.restore_files()
    logger.close_files()"""
