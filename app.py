
import streamlit as st
from gui_handler_class import GUIHandler

def main():

    gui_handler = GUIHandler(st)
    gui_handler.run()

if __name__ == "__main__":

    main()