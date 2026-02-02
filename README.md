# DPC Lab Progress Log

Welcome to my archive of experiments in Distributed and Parallel Computing. This isn't just code; it is a timeline of me figuring out how to make computers talk to each other without screaming errors.

## Current Status
**Level:** Lab 2  
**State:** Operational  
**Morale:** High

## The Log

### Lab 2: Concurrency & The Load Balancer
**Achievement Unlocked: Multitasking**

I quickly found out that a single-threaded server is about as useful as a screen door on a submarine when twenty people try to use it at once.

**The Breakdown:**
- **Threaded Server:** I implemented threading so the server can chew gum and walk at the same time. Now it can handle multiple clients without making them wait in line.
- **Load Balancing:** I built a custom TCP Load Balancer. It acts as a traffic cop, directing client requests to different backend servers using a Round Robin strategy. It is transparent, it is scalable, and it is beautiful.

### Lab 1: Foundations & RPC
**Achievement Unlocked: Hello World (Remotely)**

The beginning. I learned that localhost is home, but 127.0.0.1 is also home.

**The Breakdown:**
- **Basic Sockets:** Sending strings back and forth. It sounds simple, but getting the handshake right is an art form.
- **RPC (Remote Procedure Calls):** I successfully tricked my computer into running a function on a "server" while the "client" sat back and waited for the result.

## To Be Continued...
The journey continues. More labs, more complex architectures, and inevitably, more distributed bugs to squash.

---
*Repository maintained by ManveerAnand*

