

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b4)
(on-table b4)
(on b5 b1)
(on b6 b5)
(clear b2)
(clear b3)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b2 b6)
(on b4 b3)
(on b5 b2)
(on b6 b4))
)
)


