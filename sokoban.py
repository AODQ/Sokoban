import sys
import pygame
import tkinter
import tkinter.filedialog
import options
import game

class Sokoban:
  def __init__(self, w_width, w_height, caption):
    pygame.init()
    self.root = tkinter.Tk()
    self.root.withdraw()
    self.w_width = w_width
    self.w_height = w_height
    self.caption = caption
    self.set_window(self.w_width, self.w_height, self.caption)
    font = pygame.font.Font("Retroscape.ttf", 15)
    self.menu = []

    for i, text in enumerate(("PLAY", "EDIT", "HELP")):
      self.menu.append(options.Option(text, self.w_width/2,
               (self.w_height/4)+103+(i*50), font))

    self.title = pygame.image.load("title.png").convert()
    self.title_pos = self.title.get_rect(center=(self.w_width/2,
                           self.w_height/4))
    self.game = game.Game(self)

  def set_window(self, w_width, w_height, caption):
    # don't do this dumbass
    w_width = 640;
    w_height = 480;
    self.window = pygame.display.set_mode((w_width, w_height))
    pygame.display.set_caption(caption)

  def quit(self):
    self.root.quit()
    pygame.quit()
    sys.exit()

  def select_file(self):
    try:
      return tkinter.filedialog.askopenfilename(
        initialdir="./levels", title="Select File", filetypes=(("Sok Format",
        ["*.sok", "*.xsb", "*.txt"]), ("All Files", "*.*")))
    except tkinter.TclError:
      self.quit()

  def run(self):
    while True:
      self.window.fill((0, 0, 0))
      self.window.blit(self.title, self.title_pos)
      options.draw(self.window, self.menu)

      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
          opt = options.choice(self.menu)

          if opt:
            if opt == "PLAY":
              file_path = self.select_file()

              if file_path:
                pygame.mixer.music.load("music.mp3")
                pygame.mixer.music.play(-1)
                file_path and self.game.play(file_path)
                pygame.mixer.music.stop()

            self.set_window(self.w_width, self.w_height,
                    self.caption)

        elif event.type == pygame.VIDEORESIZE:
            self.set_window(640, 480, "hm");
        elif event.type == pygame.QUIT:
          self.quit()

      pygame.display.update()

if __name__ == "__main__":
   Sokoban(550, 350, "Sokoban - Menu").run()
