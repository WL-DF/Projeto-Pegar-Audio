import threading
import time

class ProgressManager:
    """Gerenciador de progresso com atualizações suaves."""
    
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.current_value = 0
        self.target_value = 0
        self.is_animating = False
        
    def set_progress(self, value):
        """Define o valor alvo do progresso e inicia a animação."""
        self.target_value = value
        if not self.is_animating:
            self.start_animation()
            
    def start_animation(self):
        """Inicia a animação do progresso."""
        if self.is_animating:
            return
            
        self.is_animating = True
        
        def animate():
            while self.is_animating and self.current_value < self.target_value:
                self.current_value += 1
                if self.update_callback:
                    self.update_callback(self.current_value)
                time.sleep(0.02)  # Controla a velocidade da animação
                
            # Garante que chegamos ao valor exato
            if self.current_value != self.target_value:
                self.current_value = self.target_value
                if self.update_callback:
                    self.update_callback(self.current_value)
                    
            self.is_animating = False
        
        threading.Thread(target=animate, daemon=True).start()
        
    def reset(self):
        """Reseta o gerenciador de progresso."""
        self.current_value = 0
        self.target_value = 0
        self.is_animating = False