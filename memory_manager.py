

class ActiveMemory:
    def __init__(self):
        self.clusters = []
        self.step = 0

    def add_message(self, topic, message):
        self.step += 1
        cluster = self.find_recent_match(message)
        if not cluster:
            cluster = self.find_match(message)

        if cluster:
            cluster["messages"].append(message)
            cluster["strength"] += 1
            cluster["last_seen"] = self.step
            return
        self.create_cluster(topic, message)

    def create_cluster(self, topic, message):
        cluster = {
            "topic" : topic,
            "messages" : [message],
            "strength" : 1,
            "last_seen": self.step
        }

        self.clusters.append(cluster)
    
    def get_words(self, text):
        return set(text.lower().split())
    
    def find_recent_match(self, message):
        message_words = self.get_words(message)
        best_cluster = None
        best_score = 0

        for cluster in self.clusters[-5:]:
            topic_words = self.get_words(cluster["topic"])
            score = len(topic_words & message_words)

            if score > best_score:
                best_score = score
                best_cluster = cluster

        if best_score >= 1:
            return best_cluster
        return None

    def find_match(self, message):
        message_words = self.get_words(message)

        best_cluster = None
        best_score = 0

        for cluster in self.clusters:
            topic_words = self.get_words(cluster["topic"])

            score = len(topic_words & message_words)

            if score > best_score:
                best_score = score
                best_cluster = cluster

        if best_score >= 1:
            return best_cluster

        return None