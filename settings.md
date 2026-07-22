Siamo in un computer Mac silicon M4 con 48 GB. 
Questo progetto si chiama "Impostazioni_PC" e i files che dovranno essere creati devono stare nella cartella corrente (se non diversamente specificato).
Se per il lavoro che ti chiedo hai bisogno di maggiori dettagli raccogli le informazioni che ti servono autonomamente. 
Faccio lavoro di coding con sessioni di lavoro lunghe.
Imposta nei file di configurazione del server locale ollama in ~/.pi le opzioni di default di default più opportune per i modelli locali gnorando le impostazioni attualmente presenti e ottimizzandole per le specifiche di uso richiesto e hardware disponibile.
Fai particolare attenzione alle opzioni "input", "contextWindow", "maxTokens", "reasoning", "num_ctx", "temperature", "top_p", "num_predict", "num_ctx".
Aggiusta gli stessi parametri anche nel file di configurazione ~/.pi/agent/models.json allineandolo ai modelli disponibili nel server locale ollama (vedi elenco con il comando  "ollama ls").

Crea un file Readme.html con il riepilogo e le spiegazioni dei file modificati e i parametri impostati.
Crea tutti i files necessari per il deploy in git.
Inizializza git e fai un commit del lavoro fatto.
Fai un deploy del progetto su git.ifac.cnr.it e anche sul mio github.
